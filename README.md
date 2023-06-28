# Star Organizer

It's a command-line tool that helps you organize all of your GitHub starred repositories. It generates a README.md file containing each starred repository, sorted alphabetically by category and name. Simply provide your GitHub personal access token, and let the script do the rest.

# Installation and Usage

To use the program, follow the steps below:

1. Open a terminal window.

2. Ensure that you have Python 3.x and pip installed on your machine. You can check by running the following commands:

    ```
    python --version
    pip --version
    ```

3. Install the program by navigating to the project folder and run the following command:

    ```
    pip install .
    ```

4. Once the installation is complete, you can run the program by typing the following command in your terminal:

    Linux:
    ```
    star-organizer --token <YOUR_ACCESS_TOKEN>
    ```
    Windows:
   ```
    star-organizer.exe --token <YOUR_ACCESS_TOKEN>
    ```   

    Remember to replace `<YOUR_ACCESS_TOKEN>` with your actual GitHub personal access token.

5. That's it! The program should now generate a `README.md` file in your current directory with a categorized and alphabetized list of all your starred repositories. You can place this file in its own repository and host your own personal list.