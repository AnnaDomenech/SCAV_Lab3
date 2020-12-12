from MP4container import MP4container

EXIT = 0
def one(x):
    aux= int(input("You can create the default mp4 container, or create a new customed mp4 container \nwith the default parameters (as in default case) but you also would change the parameters:\n[1]Default\n[2]Personalized\n"))
    x.finalContainerMenu(aux)
def two(x):
    x.print_files('all')
def three(x):
    h = MP4container()
    h.video= h.path / "newBBB.mp4"
    h.getBroadcastingStd()

def four(x):
    x.print_files('mp4')
    a = str(input("Choose three MP4 to check its video and audio broadcasting:\n Put a 0 to not choose a file.\n"))
    b = str(input("Second MP4 to check:\n"))
    c = str(input("Third MP4 to check:\n")) 
    if a is not '0':
        a = MP4container(name=x.files[int(a)-1][1])
        a.getBroadcastingStd()
    if b is not '0':
        b = MP4container(name=x.files[int(b)-1][1])
        b.getBroadcastingStd()
    if c is not '0':
        c = MP4container(name=x.files[int(c)-1][1])
        c.getBroadcastingStd()
       

            
def execall(argument,mp4):
    # Get the function from switcher dictionary
    func = switcher.get(argument, "nothing")
    # Execute the function
    return func(mp4)

switcher = {
        1: one,
        2: two,
        3: three,
        4: four
}

if __name__ == "__main__": 
    mp4 = MP4container()
    x = input("[1]Define MP4 Container\n[2]Display Folder files\n[3]Check Broadcasting of BBB video\n[4]Testing\n")
    while not x=='5':
         execall(int(x),mp4)
         x = input("[1]Define MP4 Container\n[2]Display Folder files\n[3]Check Broadcasting of BBB video\n[4]Testing\n[5] Exit")