#!/usr/bin/env python

#------------------------
# IMPORTATION DES MODULES

import sys
sys.path.append('.src/modules') #Pour implementer les modules dans le repertoire 'modules' 


    #--------------------
    # Modules perso
import Sequence
                                                                 
from src.modules.tools import quality_treatment, length_treatment, format_files, r_call, fastq2fasta 

    #--------------------
    # Modules cosmos
import os
import subprocess
from cosmos.api import Cosmos, draw_stage_graph, draw_task_graph, pygraphviz_available

#------------------------
# DEFINITION DU WORKFLOW 'run_test'


def run_test(execution):    
    
    #--------------------
    # Generation des graps initiaux    
    
    
    Format0 = [execution.add_task(format_files,
                                 tags = dict(path2input="testing/data/4.fastq", path2output="testing/data/formated_initial", ftype=ftype),
                                 )
                for ftype in ['quality','length']]
    GraphGen0_a = [execution.add_task(r_call,
                                   tags = dict(path2script="plot_quality_scores.R", path2input="testing/data/formated_initial_quality.txt", path2output="testing/results/initial_quality_scores.pdf" ),
                                   parents=Format0)
                    ]
    GraphGen0_b = [execution.add_task(r_call,
                               tags = dict(path2script="plot_sequence_length.R", path2input="testing/data/formated_initial_length.txt", path2output="testing/results/initial_sequence_length.pdf" ),
                               parents=Format0)
                    ]
    
    #--------------------
    # Traitement de qualite et generation des graphs After Quality Treatment (AQT)      

    QualTR = [execution.add_task(quality_treatment,
                                 tags = dict(path2file="testing/data/4.fastq", path2output="testing/data/quality_treatment_results.fastq", threshold=15)
                                 )
                    ]
        
    Format1 = [execution.add_task(format_files,
                                 tags = dict(path2input="testing/data/quality_treatment_results.fastq", path2output="testing/data/formated_AQT", ftype=ftype),
                                 parents = QualTR
                                 )
                for ftype in ['quality','length']]
    GraphGen1_a = [execution.add_task(r_call,
                                   tags = dict(path2script="plot_quality_scores.R", path2input="testing/data/formated_AQT_quality.txt", path2output="testing/results/AQT_quality_scores.pdf" ),
                                   parents = Format1)
                    ]
    GraphGen1_b = [execution.add_task(r_call,
                               tags = dict(path2script="plot_sequence_length.R", path2input="testing/data/formated_AQT_length.txt", path2output="testing/results/AQT_sequence_length.pdf" ),
                               parents = Format1)
                    ]
   
    #--------------------
    # Traitement de longueur des sequences et generation des graphs After Length Treatment (ALT)      
           
    LenTR = [execution.add_task(length_treatment,
                          tags = dict(path2file="testing/data/quality_treatment_results.fastq", path2output="testing/data/length_treatment_results.fastq", threshold=60),
                          parents = QualTR)
            ]
    
    Format2 = [execution.add_task(format_files,
                                 tags = dict(path2input="testing/data/length_treatment_results.fastq", path2output="testing/data/formated_ALT", ftype=ftype),
                                 parents = LenTR
                                 )
                for ftype in ['quality','length']]
    
    GraphGen2_a = [execution.add_task(r_call,
                                   tags = dict(path2script="plot_quality_scores.R", path2input="testing/data/formated_ALT_quality.txt", path2output="testing/results/ALT_quality_scores.pdf" ),
                                   parents = Format2)
                    ]
    GraphGen2_b = [execution.add_task(r_call,
                               tags = dict(path2script="plot_sequence_length.R", path2input="testing/data/formated_ALT_length.txt", path2output="testing/results/ALT_sequence_length.pdf" ),
                               parents = Format2)
                    ]
   
    #--------------------
    # Generation d'un fichier sortie FASTA
    
    FastaFormat = [execution.add_task(fastq2fasta,
                                     tags = dict(path2input="testing/data/length_treatment_results.fastq", path2output="testing/results/Final.fasta"),
                                     parents = LenTR)]
    #--------------------
    # Generation des schemas du workflow (si pygraphviz installe)
    
    if pygraphviz_available:
        # These images can also be seen on the fly in the web-interface
        draw_stage_graph(execution.stage_graph(), 'testing/workflow_info/test_task_graph.png', format='png')
        draw_task_graph(execution.task_graph(), 'testing/workflow_info/test_stage_graph.png', format='png')
    else:
        print 'Pygraphviz is not available :('

    execution.run(max_attempts=1, max_cores=10)
    
#------------------------
# EXECUTION DU WORKFLOW
if __name__ == '__main__':
    cosmos = Cosmos('sqlite:///%s/sqlite.db' % os.path.dirname(os.path.abspath(__file__)))
    cosmos.initdb()

    subprocess.check_call('mkdir -p testing testing/data testing/results testing/workflow_info', shell=True)
    #subprocess.check_call('cp extdata/4.fastq testing/data', shell=False)
    execution = cosmos.start('Testx', 'testing',restart=True, skip_confirm=True)
    run_test(execution)
"""else:   
    #--------------------
    # Connexion aux services cosmos (BDD)    
	cosmos = Cosmos('sqlite:///sqlite.db')
	cosmos.initdb()
	    
    #--------------------
    # Creation des sous-dossiers resultats
	subprocess.check_call('mkdir -p testing testing/data testing/results testing/workflow_info', shell=True)
	#subprocess.check_call('cp extdata/4.fastq testing/data', shell=False, stderr=subprocess.STDOUT)

    #--------------------
    # Definition de la tache et execution
	execution = cosmos.start('Test1', 'testing',restart=True, skip_confirm=True)
	run_test(execution)
"""
