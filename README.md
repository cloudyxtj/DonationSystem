## Setup Instructions
### Step 1: Download Git
1. **Download Git**:
   - Download [Git](https://git-scm.com/downloads) for your operating system.
   - Follow the installation prompts to complete the setup.

### Step 2: Configure Git Username and Email
1. **Open your terminal or command prompt**:
   - On Windows, you can use Git Bash, Command Prompt, or PowerShell.
   - On macOS or Linux, use the default terminal.

2. **Set your Git username and email**:
   - Run the following command to configure your username:
     ```bash
     git config --global user.name "Your Name"
     ```
   - Configure your email:
     ```bash
     git config --global user.email "youremail@example.com"
     ```

## Start Installation
#### 1. **Clone the Repository**

First, you need to clone the repository in any location you prefer:

```bash
git clone https://github.com/cloudyxtj/DonationSystem.git
```
Move into the directory:
```bash
cd DonationSystem
```

#### 2. **Create a Virtual Environment**
Next, you need to create a virtual environment:
```bash
# On macOS/Linux
python3 -m venv env
source env/bin/activate

# On Windows
python -m venv env
env\Scripts\activate
```
Note the `(env)` in front of the prompt after successfully activated.

#### 3. **Install Django**
Once your virtual environment is activated, install the required dependencies:
```bash
pip install django
```

#### 4. **Set Up the Database**
Now, you need to set up the database by running migrations. This will create the necessary database tables for your project:

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. **Running the Development Server**
Now that your environment is set up, you can run the Django development server:
```bash
python manage.py runserver
```

This will start the server on [http://127.0.0.1:8000](http://127.0.0.1:8000). 

Open that URL in your web browser to view the project.

#### User login credentials:

- username: donor1

- password: userDonor@111

#### 6. **Create a Superuser (Admin Account)**
To log in to the Django admin site: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

#### Admin login credentials:

- Username: admin

- Password: adminDonation@123