import os, datetime, sys, json


source_records = 0
records = 0

# Open the source file
data_path = os.path.dirname(os.path.abspath(__file__)) + "/../../../data"
solution_json_file = '{}/routesData.json'.format(data_path)
try:
    solutionRoutes = json.loads(open(solution_json_file).read())
    source_records = len(solutionRoutes.keys())
    if source_records == 0:
        print("The source file {} has empty keys".format(solution_json_file))
        sys.exit()
except Exception as e:
    print("Cannot open routeData file! {}".format(solution_json_file))
    print(str(e))
    sys.exit()
#print(solutionRoutes)


# Open the backup file
tag = datetime.date.today().strftime ("%Y%m%d")
solution_backup_json_file = '{}/routesData.json.{}'.format(data_path, tag)
isReadyToUpdate = True
try:
    if os.path.isfile(solution_backup_json_file):
        backup_solutionRoutes = json.loads(open(solution_backup_json_file).read())
        records = len(backup_solutionRoutes.keys())
        if source_records <= records:
            isReadyToUpdate = False
except Exception as e:
    print("{} is the new file".format(solution_backup_json_file))


# Backup the data if it is necessary
if isReadyToUpdate:
    try:
        with open(solution_backup_json_file, 'w') as fp:
            json.dump(solutionRoutes, fp)
        print("Backup is done")
    except Exception as e:
        print("Cannot backup routeData file! {}".format(solution_backup_json_file))
        print(str(e))
