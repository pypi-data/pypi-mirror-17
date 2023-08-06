# standard library imports
import sys, os, copy, tempfile
#from importlib import import_module
import imp
import warnings

# pypref package information imports
from __pkginfo__ import __version__


class Preferences(object):
    """
    This is pypref main preferences class definition. This class is used to create, load
    and update application's preferences dictionary in memory and in file.
    At initialization, a preferences dictionary will be pulled from the given directory
    and filename if existing. Otherwise, preferences file will be created and preferences
    dictionary will be initialized to an empty dictionary. Preferences can be 
    accessed like a dictionary or using get method.
    
    When used in python a application, it is advisable to wrap this class in a singleton
    as the following:
    
    
    .. code-block:: python
    
    
        from pypref import Preferences
        
        class MyPreferences(Preferences):
            def __new__(cls, *args, **kwds):
                thisSingleton = cls.__dict__.get("__thisSingleton__")
                if thisSingleton is not None:
                    return thisSingleton
                cls.__thisSingleton__ = thisSingleton = Preferences.__new__(cls)
                return thisSingleton
         
    
    :Parameters:
        #. directory (None, path): The directory where to create preferences file.
           If None is given, preferences will be create in user's home directory.
        #. filename (string): The preferences file name.
    """
    def __init__(self, directory=None, filename="preferences.py"):
        self.__set_directory(directory=directory)
        self.__set_filename(filename=filename)
        # load existing or create file
        self.__load_or_create()
    
    def __getitem__(self, key):
        return dict.__getitem__(self.__preferences, key)
    
    def __set_directory(self, directory):
        if directory is None:
            directory = os.path.expanduser('~')
        else:
            assert os.path.isdir(directory), "Given directory '%s' is not an existing directory"%directory
        # check if a directory is writable
        try:
            testfile = tempfile.TemporaryFile(dir = directory)
            testfile.close()
        except Exception as e:
            raise Exception("Given directory '%s' is not a writable directory."%directory)
        # set directory
        self.__directory = directory
            
    def __set_filename(self, filename): 
        assert isinstance(filename, basestring), "filename must be a string, '%s' is given."%filename
        filename = str(filename)
        assert os.path.basename(filename) == filename, "Given filename '%s' is not valid. \
A valid filename must not contain especial characters or operating system separator which is '%s' in this case."%(filename, os.sep)
        if not filename.endswith('.py'):
            filename += '.py'
            warnings.warn("'.py' appended to given filename '%s'"%filename)
        self.__filename = filename
    
    def __load_or_create(self):
        fullpath = self.fullpath
        if os.path.isfile(fullpath):
            (path, name) = os.path.split(fullpath) # to use imp instead of importlib
            (name, ext)  = os.path.splitext(name)  # to use imp instead of importlib
            (file, filename, data) = imp.find_module(name, [path]) # to use imp instead of importlib
            # try to import as python module
            try:
                #mod = import_module(fullpath)
                mod = imp.load_module(name, file, filename, data)
            except Exception as e:
                raise Exception("Existing file '%s' is not a python importable file (%s)"%(fullpath, e))
            # check whether it's a pypref module
            try:
                version     = mod.__pypref_version__
                preferences = mod.preferences
            except Exception as e:
                raise Exception("Existing file '%s' is not a pypref file (%s)"%(fullpath, e))
            # check preferences
            assert isinstance(preferences, dict), "Existing file '%s' is not a pypref file (%s)"%(fullpath, e)
            self.__preferences = preferences
        else:
            self.__dump_file(preferences = {})  
            self.__preferences = {}      
            
    def __get_normalized_string(self, s):
        stripped = s.strip()
        if not stripped.startswith('"') and not stripped.endswith('"'):
            if not stripped.startswith("'") and not stripped.endswith("'"):
                if "'" in s:
                    s = '"%s"'%s
                else:
                    s = "'%s'"%s
        return s
                         
    def __dump_file(self,  preferences, temp=False):
        if temp:
            try:
                fd = tempfile.NamedTemporaryFile(dir=tempfile._get_default_tempdir(), delete=True)
            except Exception as e:
                raise Exception("unable to create preferences temporary file. (%s)"%e)
        else:
            # try to open preferences file
            try:
                fd = open(self.fullpath, 'w')
            except Exception as e:
                raise Exception("Unable to open preferences file '%s."%self.fullpath)
        # write preferences
        lines  = "# This file is an automatically generated pypref preferences file. \n\n" 
        lines += "__pypref_version__ = '%s' \n\n"%__version__ 
        lines += "preferences = {}" + "\n"
        for k, v in preferences.items():
            if isinstance(k, basestring):
                k = self.__get_normalized_string(k)
            print v
            print isinstance(v, basestring)
            if isinstance(v, basestring):
                v = self.__get_normalized_string(v)
            lines += "preferences[%s] = %s\n"%(k, v)
        # write lines  
        try:     
            fd.write(lines) 
        except Exception as e:
            raise Exception("Unable to write preferences to file '%s."%self.fullpath)
        # close file
        fd.close()
    
    @property
    def directory(self):
        """Preferences file directory."""
        return copy.deepcopy(self.__directory)
    
    @property
    def filename(self):
        """Preferences file name."""
        return copy.deepcopy(self.__filename)
    
    @property
    def fullpath(self):
        """Preferences file full path."""
        return os.path.join(self.__directory, self.__filename)
    
    @property
    def preferences(self):
        """Preferences dictionary copy."""
        return copy.deepcopy(self.__preferences)
            
    def get(self, key, default=None):
        """
        Get the preferences value for the given key. 
        If key is not available then returns default value None.
        
        :Parameters:
            #. key (object): The Key to be searched in the preferences.
            #. default (object): The Value to be returned in case key does not exist.
        
        :Returns:
            #. value (object): The value of the given key or given default value is 
               key does not exist.
        """
        return self.__preferences.get(key, default)
        
    def check_preferences(self, preferences):
        """
        This is an abstract method to be overloaded if needed. 
        All preferences setters such as set_preferences and update_preferences
        call check_preferences prior to setting anything. This method returns 
        a check flag and a message, if the flag is False, the message is raised 
        as an error like the following.
        
        .. code-block:: python
    
            flag, m = self.check_preferences(preferences)
            assert flag, m
        
        
        :Parameters:
            #. preferences (dictionary): The preferences dictionary.
        
        :Returns:
            #. flag (boolean): The check flag.
            #. message (string): The error message to raise.
            
        """
        return True, ""
        
    def set_preferences(self, preferences):
        """
        Set preferences and update preferences file.
        
        :Parameters:
            #. preferences (dictionary): The preferences dictionary.
        """
        flag, m = self.check_preferences(preferences)
        assert flag, m
        assert isinstance(preferences, dict), "preferences must be a dictionary"
        # try dumping to temp file first
        try:
            self.__dump_file(preferences, temp=True)
        except Exception as e:
            raise Exception("Unable to dump temporary preferences file (%s)"%e)
        # dump to file
        try:
            self.__dump_file(preferences, temp=False)
        except Exception as e:
            raise Exception("Unable to dump preferences file (%s). Preferences file can be corrupt, but in memory stored preferences are still available using and accessible using preferences property."%e)
        # set preferences
        self.__preferences = preferences
    
    def update_preferences(self, preferences):
        """
        Update preferences and update preferences file.
        
        :Parameters:
            #. preferences (dictionary): The preferences dictionary.
        """
        flag, m = self.check_preferences(preferences)
        assert flag, m
        assert isinstance(preferences, dict), "preferences must be a dictionary"
        newPreferences = self.preferences
        newPreferences.update(preferences)
        # set new preferences
        self.set_preferences(newPreferences)
        
            
            
            
            
            
            
        
        
        