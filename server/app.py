from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)


def generate_random_string(length=10):
    """Generates a random string of the specified length."""
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(chars) for _ in range(length))

def generate_random_integer(min_value=0, max_value=100):
    """Generates a random integer between the specified minimum and maximum values."""
    return random.randint(min_value, max_value)

# Define the endpoint for screen recording submissions
@app.route('/submit-recording', methods=['POST'])
def submit_recording():
    
    try:
        # Handle the incoming screen recording data
        #recording_file = request.files['recording'] #data is sent as a file upload
        recording_data = request.data #data is sent as raw binary data
        # You may need to save it to the 'recordings' directory or process it as needed
        random_string = generate_random_string()
        filename = f"my_file_{random_string}+.mp4"
        with open('recordings/{filename}', 'wb') as file: #receive the data as raw binary data
            file.write(recording_data)

        recording_file.save('recordings/{filename}')

        # You can access the recording data using request.files or request.data
        # Perform any necessary processing or compression here
        
        # Respond with a success message upon successful submission
        return jsonify({'message': 'Screen recording submitted successfully'}), 200
    except Exception as e:
        # Handle errors gracefully and provide appropriate feedback
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
