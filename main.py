import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Welcome<h1>"

# 1. Registering a student as a voter.
# a. It will be necessary for new students to be registered to vote.
@app.route("/register", methods = ['GET', 'POST'])
def register():
    voterId = request.args.get('voterId')
    name = request.args.get('name')
    email = request.args.get('email')
    yeargroup =  request.args.get('yeargroup')
    contact = request.args.get('contact')
    major = request.args.get('major')



    voter = {
                'voterId' : voterId,
                'name' : name,
                'email' : email,
                'yeargroup' : yeargroup,
                'contact' : contact,
                'major' : major

            }
    
    with open('./tmp/data.txt', 'a') as f:
        f.write(json.dumps(voter) + '\n')
    
    return jsonify({'status': '200 Ok'})

# 2. De-registering a student as a voter.
# a. A student may need to be de-registered once they leave campus.
@app.route("/deregister", methods = ['GET', 'DELETE'])
def delete():
    voterId = request.args.get('voterId')
    data = [] 

    with open('./tmp/data.txt', 'r') as f:
        for line in f:
            dict = json.loads(line)
            data.append(dict)

    new_dict = [d for d in data if d.get('voterId') != voterId]


    with open('./tmp/data.txt', 'w') as f:
      for i in new_dict:
        f.write(json.dumps(i) + '\n')
    
    return jsonify({'status': '200 Ok'})
# 3. Updating a registered voter’s information.
# a. A student’s year group, major or other information might change.
@app.route('/edit-voter', methods=['GET', 'PUT'])
def update_data():
    voterId = request.args.get('voterId')
    major = request.args.get('major')
    contact = request.args.get('contact')

    # Load JSON objects from file
    with open('./tmp/data.txt', 'r') as file:
        data_list = [json.loads(line) for line in file if line.strip()]

    updated_obj = None
    for obj in data_list:
        if obj["voterId"] == voterId:
            # Update the "major" and "contact" keys in the dictionary
            obj["major"] = major
            obj["contact"] = contact
            new_obj = obj
            break
    
    if new_obj:
        # Create a list with the new object
        responseData = [new_obj]
    else:
        # If voterId does not exist
        responseData = []
    
    with open('./tmp/data.txt', 'w') as file:
      for i in data_list:
        file.write(json.dumps(i) + '\n')

    # Return the updated object as a JSON response
    return jsonify(responseData)

    



# 4. Retrieving a registered voter.
@app.route('/view-voter', methods=['GET'])
def view_voter():  
    voterId = request.args.get('voterId')

    with open('./tmp/data.txt', 'r') as file:
        data_list = [json.loads(line) for line in file if line.strip()]
    

    new_obj = None
    for obj in data_list:
        if obj["voterId"] == voterId:
            new_obj = obj
            break
    
    if new_obj:
        # Create a list with the new object

        responseData = [new_obj]
    else:
        # If voterId does not exist
        responseData = []
    
    return jsonify(responseData)
# 5. Creating an election.
@app.route('/new-election', methods=['GET', 'POST'])
def create_election():  
    ElectionId = request.args.get("ElectionId")
    Election = request.args.get("Election")
    Year = request.args.get("Year")
    Position = request.args.get("Position")
    Candidate = request.args.get("Candidate")
    count = request.args.get("count")
   

    elections =  {
                    "ElectionId" : ElectionId,
                    "Election" : Election,
                    "Year" : Year,
                    "Position" : Position,
                    "Candidate" : Candidate,
                    "count" : count
                }

    with open('./tmp/electionsData.txt', 'a') as f:
        f.write(json.dumps(elections) + '\n')
    
    return jsonify({'status': '200 Ok'})


# 6. Retrieving an election (with its details).
@app.route('/view-election', methods=['GET'])
def view_election():  
    ElectionId = request.args.get('ElectionId')

    with open('./tmp/electionsData.txt', 'r') as file:
        data_list = [json.loads(line) for line in file if line.strip()]
    

    new_obj = None
    for obj in data_list:
      if obj["ElectionId"] == ElectionId:
          new_obj = obj
          break
    if new_obj:
        # Create a list with the new object
      responseData = [new_obj]
    else:
        # If voterId does not exist
        responseData = []
    
    return jsonify(responseData)

# 7. Deleting an election.
@app.route("/delete-election", methods = ['GET', 'DELETE'])
def delete_election():
    ElectionId = request.args.get('ElectionId')
    data = [] 

    with open('./tmp/electionsData.txt', 'r') as f:
        for line in f:
            dict = json.loads(line)
            data.append(dict)

    data_list = [d for d in data if d.get('ElectionId') != ElectionId]


    with open('./tmp/electionsData.txt', 'w') as f:
      for i in data_list:
              f.write(json.dumps(i) + '\n')    
    return jsonify({'status': '200 Ok'})
# 8. Voting in an election.
@app.route("/vote", methods = ['GET', 'PUT'])
def vote():
    ElectionId = request.args.get('ElectionId')
    Candidate = request.args.get('Candidate')

    # Load JSON objects from file
    with open('./tmp/electionsData.txt', 'r') as file:
        data_list = [json.loads(line) for line in file if line.strip()]

    new_obj = None
    for obj in data_list:
        if obj["ElectionId"] == ElectionId:
            # Update the "major" and "phone-number" keys in the dictionary
            obj["count"] = str(int(obj["count"]) + 1)
            new_obj = obj
            break
    
    if new_obj:
        # Create a list with the new object
        responseData = [new_obj]
    else:
        # If voterId does not exist
        responseData = []
    
    with open('./tmp/electionsData.txt', 'w') as file:
      for i in data_list:
        file.write(json.dumps(i) + '\n')

    # Return the updated object as a JSON response
    return jsonify(responseData)

if __name__ == '__main__':
    app.debug = True
    app.run()

