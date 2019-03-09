# Setup Instructions 
Note all setup is done with Python3

### Needed Python3 Packages 
Run the following commands to install needed packages
> pip3 install thesaurus==0.2.3 

### Running Setup
To run setup.py no arguments are needed. Run the following command:
> python3 setup.py

If the table files are not present in the setup folder, this will 
create the needed files (table_StartWords.txt, table_SynWords.txt, 
and table_AnyWords.txt). You can expect this process to take around 
3 minutes. 
The script will then add the data from these generated files to the database 
init.db 