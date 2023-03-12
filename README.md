# podcasts-finder
 
Hey there!

You have found the repo where Lyna Benyahia and Jason Morel will work on their programming project.

We noticed that it is not possible to sort podcasts by duration on the Spotify app.
Therefore, the idea is to build a tool which will help finding podcasts depending on their theme AND duration. 
Results will be sent through Telegram so that users can open links from their phone.

## How to use our tool

We'll consider that Python is allready installed on your computer. 
If not, you can get started here: https://www.anaconda.com/products/distribution.

1. Fork our repo OR download it as a .zip folder;

    ![Download repo](/presentation/images/download_repo.png?raw=true "Download repo as .zip")

2. You could unzip the downloaded file where you keep all your Github repositories.
But you can also store it somewhere else, it's up to you.

3. Then open the file 'podcasts-tracker-main' and copy its path;

    ![Copy path](/presentation/images/copy_address.png?raw=true "Copy path")
    
4. Now, open your command prompt;

5. Copy, paste and run the following lines to install 'spotipy' and 'request' packages:
    + For Windows users:
        ```bash
        py -m pip install spotipy
        py -m pip install request
        ```
    + For everyone else:
        ```bash
        pip install spotipy
        pip install request
        ```

6. Stay in your command prompt and:
    + type 'cd ' and paste the path of the folder 'podcast-tracker-main'. Then press return to run;
    + type 'python podcast_finder.py' and press return.
    
7. You should see this window now:
    
    ![User interface](/presentation/images/user_interface.png?raw=true "User interface")

## How the project is built

We divided the project in several .py files.
Each file defines functions for specific parts of the project.
See details below:
* episode_treatment.py interacts with Spotify API to search for episodes;
* show_treatment.py interacts with Spotify API to search for shows;
* send_message.py defines how to send messages through Telegram;
* podcast_finder.py puts together the 3 files listed above and manages user interface.