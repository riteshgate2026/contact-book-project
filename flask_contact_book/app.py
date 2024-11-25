from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dictionary to store contacts in memory
contacts = {}


@app.route('/')
def home():
    return render_template('index.html', contacts=contacts)


@app.route('/save_contact', methods=['GET', 'POST'])
def save_contact():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        mobile = request.form['mobile']

        # Check if contact already exists
        if name in contacts:
            return "Contact already exists!"

        contacts[name] = {'age': age, 'email': email, 'mobile': mobile}
        return redirect(url_for('home'))  # Redirect to home page after saving contact

    return render_template('save_contact.html')  # Render the form for adding a new contact


@app.route('/update_contact/<contact_name>', methods=['GET', 'POST'])
def update_contact(contact_name):
    if contact_name not in contacts:
        return "Contact not found!"

    contact = contacts[contact_name]

    if request.method == 'POST':
        contact['age'] = request.form['age']
        contact['email'] = request.form['email']
        contact['mobile'] = request.form['mobile']
        return redirect(url_for('home'))  # Redirect to home page after updating contact

    return render_template('update_contact.html', contact_name=contact_name, contact=contact)


@app.route('/delete_contact/<contact_name>')
def delete_contact(contact_name):
    if contact_name in contacts:
        del contacts[contact_name]
    return redirect(url_for('home'))  # Redirect to home page after deleting the contact


if __name__ == '__main__':
    app.run(debug=True)
