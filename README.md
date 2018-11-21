# Item Catalog

Item Catalog is the second project in the Full-Stack Engineer Nanodegree in Udacity.

## Project Summary

The project displays the categories in a catalog and the items related to that category. The user can log in into the catalog by signing in with a Google Account. From there, the user will be able to updated, delete, and even add new items to any category. They can only do any operation on items if they are logged in. 

The application will allow the user to:

1. View categories and items in these categories
2. Add items into categories (User logged in only)
3. Edit items (User logged in only)
4. Delete items (User logged in only)

## Requirements

You should have the following to run the project:

[Vagrant](https://www.vagrantup.com/) - A virtual environment builder and manager.

[VirtualBox](https://www.virtualbox.com/) - An open source virtualization product by Oracle.

[Git](http://git-scm.com/) - An open source version control system (VCS).

[Python3](https://www.python.org/downloads/release/python-371/) - The code uses version 3.7.1 of Python

**Important Notes:**
1. For Mac and Linux users, the default terminal works fine. For Windows users, Git Bash is recommended.
2. Up to date, VirtualBox Version 5.1 is the most stable with the Vagrant environment.
3. If you are running on a Windows Operating System, Vagrant Version 1.9.2 is the most stable.

## Running the Code
To run the code, follow the steps below:

1. Download Python3 from the link in the Requirements to Run section.

2. Download and install Vagrant and VirtualBox. If you are running a Windows Operating System, Vagrant Version 1.9.2 is the most stable.

3. Download the [VagrantFile](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile)for running the preconfigured Vagrant settings. Place it into a folder. Call it whatever you want.

4. Download or clone this repository.

5. Place this repository in the same directory as the VagrantFile.

5. Open a bash terminal and `cd` into the folder you placed your VagrantFile in.

6. Run the command `vagrant up`. For Windows users, Git is the recommended terminal.

7. Once vagrant is installed successfully, run the command `vagrant ssh` to start up the virtual environment.

8. Once the command starts with vagrant, `cd` into the vagrant directory.

9. `cd` into the item-catalog directory.

10. Run the command `python3 app.py` to run the application.



##  References

The following list is the references used in working on this project:

[Udacity Lessons on FSND]

[W3Schools](https://www.w3schools.com/css/default.asp)

[Milligram](https://milligram.io/)
