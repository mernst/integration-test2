import shutil, os
import pa2checker
import common

def run_pa2checker(annotations):
  pa2checker.revert_checker_source()

  for annotation, classes in annotations.iteritems():
    pa2checker.create_type_annotation(annotation)
    pa2checker.update_ontology_utils(annotation, classes)
  pa2checker.recompile_checker_framework()

def run_inference(project):
  common.setup_checker_framework_env()

  classpath = os.path.join(os.environ['JSR308'], 'generic-type-inference-solver', 'bin')
  if os.environ.get('CLASSPATH'):
    os.environ['CLASSPATH'] += ':' + classpath
  else:
    os.environ['CLASSPATH'] = classpath

  project_dir = common.get_project_dir(project)
  annotation_dir = os.path.join(project_dir, common.DLJC_OUTPUT_DIR, 'annotations')

  if os.path.isdir(annotation_dir):
    shutil.rmtree(annotation_dir)

  common.run_dljc(project,
                  ['inference'],
                  ['--solverArgs=backEndType=maxsatbackend.MaxSat',
                   '--checker', 'ontology.OntologyChecker',
                   '--solver', 'constraintsolver.ConstraintSolver',
                   '-m', 'ROUNDTRIP',
                   '--cache',
                   '-afud', annotation_dir])


def run(project_list):
  annotations = { "Sequence": ['java.util.List', 'java.util.LinkedHashSet'] }

  run_pa2checker(annotations)

  for project in project_list:
    common.clean_project(project)
    run_inference(project)

if __name__ == "__main__":
  run(['Sort07', 'Sort09', 'Sort10'])
