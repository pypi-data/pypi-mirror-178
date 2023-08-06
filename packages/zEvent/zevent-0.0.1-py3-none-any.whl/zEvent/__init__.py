class Event:
  def __init__(self, onActive: list = []) -> None:
    self.onActive = onActive
  
  def Add(self, event: function):
    """
    The Add function adds a function to the onActive list.
    
    
    Parameters
    ----------
        self
            Access the properties and methods of the class
        event:function
            Specify the function that should be called when the event occurs
    
    Returns
    -------
    
        The onactive list with the event added to it
    
    Doc Author
    ----------
        zCloze
    """
    self.onActive.append(event)
    return self.onActive
  def Remove(self, index: int):
    """
    The Remove function removes a given index from the onActive list.
       
    
    Parameters
    ----------
        self
            Reference the object itself
        index:int
            Specify which item to remove from the list
    
    Returns
    -------
    
        The list with the element removed
    
    Doc Author
    ----------
        zCloze
    """
    self.onActive.remove(self.onActive[index])
    return self.onActive
  def Clear(self):
    """
    The Clear function clears the onActive event, which is used to signal that a new 
    message has been received and the queue should be cleared. This function is called by 
    the main thread when it receives a message from the client indicating that all previous 
    messages have been received.
    
    Parameters
    ----------
        self
            Refer to the object that is calling the method
    
    Returns
    -------
    
        The boolean value of false
    
    Doc Author
    ----------
        zCloze
    """
    self.onActive.clear()
  def __len__(self): return len(self.onActive)
  
  def Active(self): [active() for active in self.onActive]