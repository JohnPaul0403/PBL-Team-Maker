from Database import professors_database as pd

def get_proffesor (prof_id_input):
    profs = pd.read_professors()

    for row in profs:
        name, prof_id, students = row
        if prof_id == prof_id_input:
            return {
                'status' : True,
                'data' : {
                    "name" : name,
                    "id" : prof_id
                }
            }
        
    return {
        'status' : False,
        'message' : 'data not found'
    }