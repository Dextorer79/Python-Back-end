from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Path to the JSON file
DATA_FILE = "students.json"

# Helper function to load data from the JSON file
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Helper function to save data to the JSON file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Route to get all students
@app.route("/students", methods=["GET"])
def get_students():
    data = load_data()
    return jsonify(data)

# Route to add a new student
@app.route("/students", methods=["POST"])
def add_student():
    data = load_data()
    new_student = request.json
    student_id = str(new_student.get("id"))
    if not student_id or student_id in data:
        return jsonify({"error": "Invalid or duplicate student ID"}), 400
    data[student_id] = new_student
    save_data(data)
    return jsonify({"message": "Student added successfully"}), 201

# Route to update or remove a student
@app.route("/students/<student_id>", methods=["PUT", "DELETE"])
def modify_student(student_id):
    data = load_data()
    if student_id not in data:
        return jsonify({"error": "Student not found"}), 404

    if request.method == "PUT":
        updated_student = request.json
        data[student_id] = updated_student
        save_data(data)
        return jsonify({"message": "Student updated successfully"}), 200

    elif request.method == "DELETE":
        del data[student_id]
        save_data(data)
        return jsonify({"message": "Student removed successfully"}), 200
    
# Route to create a new student using specific logic and add them
@app.route("/students/compose", methods=["POST"])
def compose_and_add_student():
    data = load_data()
    students = list(data.values())
    if len(students) < 3:
        return jsonify({"error": "Not enough students to compose a new one."}), 400
    # Sort students by ID (as integers)
    students.sort(key=lambda s: int(s["id"]))
    first_name = students[0]["first_name"]
    last_name = students[-1]["last_name"]
    age = students[1]["age"]  # any other student, e.g. second one
    # Create a new unique ID
    new_id = str(max(int(s["id"]) for s in students) + 1)
    new_student = {
        "id": new_id,
        "first_name": first_name,
        "last_name": last_name,
        "age": age
    }
    data[new_id] = new_student
    save_data(data)
    return jsonify({
        "message": "Composed and added new student successfully.",
        "student": new_student
    }), 201

if __name__ == "__main__":
    app.run(debug=True)
