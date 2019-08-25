import analyze_project
import analyze_results

# -- Set these parameters ---
DESIGNITEJAVA_PATH = r"/Users/Workspace/DJ/install/DesigniteJava.jar"
SRC_PATH = r'/Users/Workspace/jenkins'
TEMP_PATH = r'/Users/Workspace/temp'
OUT_PATH = r'/Users/Workspace/jenkins_analysis'
MAX_VERSIONS_TO_ANALYZE = 10

versions = analyze_project.analyze_multiple_versions(SRC_PATH,
                                                     OUT_PATH,
                                                     TEMP_PATH,
                                                     MAX_VERSIONS_TO_ANALYZE,
                                                     DESIGNITEJAVA_PATH)
analyze_results.summarize(OUT_PATH, versions)