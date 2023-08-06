import os
from threading import Thread
import pygame
from zEvent import Event

pygame.mixer.init()


class Sound:
  def __init__(self, filename: str):
    """
    The __init__ function is called automatically every time the class is instantiated. 
    It sets up all of the attributes in the instance, and then initializes them to their default values (if any). 
    It's important to remember that all methods in a class will take self as their first argument, just like __init__ does.
    
    Parameters
    ----------
        self
            Reference the object itself
        filename:str
            Store the filename of the sound file
    
    Returns
    -------
    
        Nothing
    
    Doc Author
    ----------
        zCloze
    """
    if not os.path.exists(filename):
      raise FileNotFoundError(f"Not found '{filename}' file at '{os.getcwd()}'")

    self.__pgs = pygame.mixer.Sound(filename)
    
    self.OnPlay = Event() # DONE
    
    self.OnStart = Event() # DONE
    self.OnStop  = Event() # DONE
    
    self.OnPause = Event() # DONE
    self.OnResume = Event()
    
    self.OnEnd = Event() # DONE
  
  def Play(self, loops: int = 1):
    """
    The Play function plays the sound.
       
    
    Parameters
    ----------
        self
            Reference the object instance
        loops:int=1
            Tell the play function how many times to loop the sound
            INFINITY_LOOPS for infinite loops
    
    Returns
    -------
    
        Nothing
    
    Doc Author
    ----------
        zCloze
    """
    def play():
      self._pgs_played = self.__pgs.play(loops)
      self.OnStart.Active()
      
      while self._pgs_played.get_busy(): self.OnPlay.Active()
      
      self.OnEnd.Active()
    
    Thread(target=play).start()
    self._pgs_played: pygame.mixer.Channel
  def Stop(self):
    """
    The Stop function stops the sound.
    
    
    Parameters
    ----------
        self
            Access the attributes and methods of the class in python
    
    Returns
    -------
    
        Nothing
    
    Doc Author
    ----------
        zCloze
    """
    self.__pgs.stop()
    self.OnStop.Active()
  def Pause(self):
    """
    The Pause function pauses the sound.
    
    
    Parameters
    ----------
        self
            Access the object's attributes
    
    Returns
    -------
    
        Nothing
    
    Doc Author
    ----------
        zCloze
    """
    if not hasattr(self, "_pgs_played"):
      raise Exception(f"Pause called without play")

    self._pgs_played.pause()
    self.OnPause.Active()
  def Resume(self):
    """
    The Resume function resumes the sound from where it was paused.
    
    
    Parameters
    ----------
        self
            Access the class attributes
    
    Returns
    -------
    
        Nothing
    
    Doc Author
    ----------
        zCloze
    """
    if not hasattr(self, "_pgs_played"):
      raise Exception(f"Resume called without play")

    self._pgs_played.unpause()
    self.OnResume.Active()

INFINITY_LOOPS = -1
