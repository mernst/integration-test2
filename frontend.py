import sys, os, shutil

import inv_check
import insert_jaif
import ontology_to_daikon
import pa2checker

import backend
import common
import argparse
sys.path.insert(0, 'simprog')
from similarity import Similarity


def compute_daikon_invariants(project_list):
  ordering_operator = "<="

  ontology_invariant_file = "TODO_from_Howie.txt"
  with open(ontology_invariant_file, 'w') as f:
    f.write(ordering_operator)

  invariant_name = "TODO_sorted_sequence"

  daikon_pattern_java_file = ontology_to_daikon.create_daikon_invariant(ontology_invariant_file, invariant_name)

  """ Search for methods that have a return type annotated with Sequence
  and for which we can establish a sortedness invariant (may done by LB).
  INPUT: dtrace file of project
         daikon_pattern_java_file that we want to check on the dtrace file.
  OUTPUT: list of ppt names that establish the invariant. Here a ppt
  is a Daikon program point, s.a. test01.TestClass01.sort(int[]):::EXIT
  Note: this step translate the type_invariant into a Daikon
  template (which is a Java file).
  """

  pattern_class_name = invariant_name
  pattern_class_dir = os.path.join(common.WORKING_DIR, "invClass")
  if os.path.isdir(pattern_class_dir):
    shutil.rmtree(pattern_class_dir)
  os.mkdir(pattern_class_dir)

  cmd = ["javac", "-g", "-classpath", common.get_jar('daikon.jar'),
         daikon_pattern_java_file, "-d", pattern_class_dir]
  common.run_cmd(cmd)

  list_of_methods = []
  for project in project_list:

    dljc_dir = common.get_dljc_dir_for_project(project)
    i=0
    while True:
      i+=1
      dtrace_dir = os.path.join(dljc_dir, "test-classes{}".format(i))
      dtrace_file = os.path.join(dtrace_dir, 'RegressionTestDriver.dtrace.gz')
      if not os.path.isfile(dtrace_file):
        print ("No dtrace file found at {0}".format(dtrace_file))
        break
    
      ppt_names = inv_check.find_ppts_that_establish_inv(dtrace_file, pattern_class_dir, pattern_class_name)
      methods = set()
      for ppt in ppt_names:
        method_name = ppt[:ppt.find(':::EXIT')]
        methods.add(method_name)
      list_of_methods +=[(project, methods)]

  print ("\n   ************")
  print ("The following corpus methods return a sequence sorted by {}:".format(ordering_operator))
  for project, methods in list_of_methods:
    if len(methods)>0:
      print (project)
      for m in methods:
        print("\t{}".format(m))
  print ("\n   ************")

  shutil.rmtree(pattern_class_dir)



def check_similarity(project, result_file, kernel_file, cluster_json=None):
  """ SUMMARY: use case of the user-driven functionality of PASCALI.
  """
  dot_to_method_map = {}
  corpus_dot_to_method_map = {}
  corpora = common.LIMITED_PROJECT_LIST

  # fetch various method information from each project in the list
  output_dir = common.DOT_DIR[project]
  method_file = common.get_method_path(project, output_dir)

  if not os.path.isfile(method_file):
    pass

  with open(method_file, "r") as mf:
    content = mf.readlines()
    for line in content:
      line = line.rstrip()
      items = line.split('\t')
      method_name = items[0]
      method_dot = items[1]
      method_dot_path = common.get_dot_path(project, output_dir, method_dot)
      corpus_dot_to_method_map[method_dot_path] = method_name

  # check similarity
  sim = Similarity()
  sim.read_graph_kernels(kernel_file)
  top_k = 5 # top k most similar methods
  iter_num = 3 # number of iteration of the WL-Kernel method
  fo = open(result_file, 'w')
  for dot_file in corpus_dot_to_method_map.keys():
    result_program_list_with_score = sim.find_top_k_similar_graphs(dot_file, dot_file, top_k, iter_num, cluster_json)
    line = dot_file+":\n"
    for (dot, score) in result_program_list_with_score:
      line += dot+ " , " + str(score) + "\n"      
    line += "\n"
    fo.write(line)
  fo.close()

def run(project_list, args, kernel_dir):
  for project in project_list:
    result_file = os.path.join(common.WORKING_DIR, args.dir, project+"_result.txt")
    kernel_file = os.path.join(common.WORKING_DIR, kernel_dir, project+"_kernel.txt")
    check_similarity(project, result_file, kernel_file, args.cluster)

    compute_daikon_invariants(project_list)

