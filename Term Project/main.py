from cmu_112_graphics import *
import random
import math

##########################################
# Game Mode
##########################################
class Player():
    def __init__(self, x,y):
        self.x=x//2
        self.y=y
        self.dx=30

    def getLocation(self):
        return (self.x, self.y)

class Enemy:
    def __init__(self, x,y,health,speed):
        self.x=x
        self.y=y
        self.health=health
        self.dy=speed/4
  
    def falling(self):
        self.y+=self.dy
        


    def moveEnemyBullet(self):
        EnemyBulletDown=self.dy*10
        self.y+=EnemyBulletDown
        
        # return self.x,self.y
    def reduceHealth(self):
        self.health-=25


    def __repr__(self):
        return f'dog location is {self.getLocation()}'
    def hitGround(self):
        if self.y>=650:
            return True


class Bullet:
    def __init__(self,x,y):
        self.x=x
        self.y=y  
        self.dy=20

    def moveBullet(self):
        self.y-=self.dy
    
    def getLocation(self):
        return (self.x, self.y)

    def __repr__(self):
        return f'fish location is {self.getLocation()}'


    def hitEnemy(self,enemy):
        fishx,fishy=self.x,self.y
        if enemy!=None:
            dogx,dogy=enemy.x,enemy.y
          
            d=50
            if dogx-d<=fishx<=dogx+d and dogy-d<=fishy<=dogy+d:
                return True
    def moveBack(self,x):
        dx=x-self.x
        if dx<0:
            self.x-=abs(dx)*0.2
           
        else:
            self.x+=abs(dx)*0.2
        self.moveBullet()


class PathFindBullet(Bullet):
    def __init__(self,x,y):
        self.x=x
        self.y=y 
     

    def moveTowards(self,target):
        if target!=None:
            dogx,dogy=target.x,target.y
            dx=(dogx-self.x)/10
            dy=(dogy-self.y)/30
            self.x+=dx
            self.y+=dy
       
    def findEnemy(self,enemy):
        fishx,fishy=self.x,self.y
        dogx,dogy=enemy.x,enemy.y
        return math.sqrt((fishx-dogx)**2+(fishy-dogy)**2)
    
    def hitEnemy(self,target):
        return super().hitEnemy(target)
       
class SuperBullet(Bullet):
    def __init__(self,x,y):
        super().__init__(x,y)
       
        self.leftx=self.x-10
        self.lefty=self.y
        self.rightx=self.x+10
        self.righty=self.y

    def getLocation(self):
        return super().getLocation() 

    def moveUp(self):
        self.y-=7
       


    def moveLeft(self):

        self.leftx-=5
        self.lefty-=0.05*self.x

    def moveRight(self):
        self.rightx+=5
        self.righty-=0.05*self.x
        
  
    def hitEnemy(self,enemy):
        dogx,dogy=enemy.x, enemy.y

        d=30
        x,y=self.x,self.y
        leftx,lefty=self.leftx,self.lefty
        rightx,righty=self.rightx, self.righty
        if (dogx-d<=x<=dogx+d and  dogy-d<=y<=dogy+d)\
            or (dogx-d<=leftx<=dogx+d and  dogy-d<=lefty<=dogy+d)\
            or (dogx-d<=rightx<=dogx+d and  dogy-d<=righty<=dogy+d):
            return True

    def move(self):
        self.moveUp()
        self.moveLeft()
        self.moveRight()

    def moveBack(self,x):
        dx=x-self.x
      
        if dx<0:
            self.x-=abs(dx)*0.2
            self.leftx-=abs(dx)*0.2
            self.rightx-=abs(dx)*0.2
        else:
            self.x+=abs(dx)*0.2
            self.leftx+=abs(dx)*0.2
            self.rightx+=abs(dx)*0.2
        
        self.moveUp()
      



def gameMode_redrawAll(app, canvas):
    font = 'Times 26 bold'
    
    catx,caty=app.cat.x,app.cat.y
    #######Display SCORE
    canvas.create_text(app.width/2, 20, text=f'$$$: {app.score}',
                        font=font, fill='Slategray1')
    canvas.create_image(550,50,image=app.buyButton)
    #######Display PathFinding Bullets Time                  
    canvas.create_text(app.width/2, 40, text=f'PathFinding Bullet: {app.pathFindTimes} times',
                        font=font, fill='Slategray1')
    
    

    if app.wantToBuy:
        if app.score>50:
            buyPage(app,canvas)
        else:
            cannotAfford(app,canvas)


    gameMode_drawDog(app,canvas)
    canvas.create_image(catx,caty,image=app.imagecat)
    gameMode_drawCatHealth(app,canvas)
 
    if app.setTypicalFish and not app.pause:
        gameMode_drawFish(app,canvas)
    
 
############3
    if app.setSuper and not app.pause:
        gameMode_drawSuperFish(app,canvas)
###############draw PATH FIND
    if app.setPathFind and app.drawPathFind and not app.pause:
        r=10
        for pffish in app.pathFindBullet:
            x,y=pffish.x,pffish.y
            canvas.create_oval(x-r,y-r,x+r,y+r,fill='purple')

############
    if not app.pause:
        for dogbullet in app.dogBullet:
            x,y=dogbullet.x,dogbullet.y
            dr=5
            canvas.create_rectangle(x-dr,y-dr,x+dr,y+dr,fill='green')


def gameMode_timerFired(app):
    if not app.pause and not app.endGame:
        app.timePassed+=50
        if app.timePassed%1000==0:
            if app.setSuper or app.pathFindTimes>=8:
                app.health=100

            else:
                app.health=50

            gameMode_dropDog(app)
        gameMode_moveDog(app)
    
        if app.setPathFind:
            if app.timePassed%150==0:
                gameMode_shootPathFindFish(app)
            gameMode_movePathFindFish(app,app.target)
            checkPathFindCollision(app,app.target)

    
    #####super fish/bullet
        if (app.score>=150 and app.superTime<=20000) or app.buySuper: 
            app.setSuper=True
            app.setTypicalFish=False
            app.superTime+=200
    
            if app.superTime>20000:
                app.buySuper=False
                app.setSuper=False
            if app.timePassed%150==0:
                gameMode_shootSuperFish(app)
            gameMode_moveSuperFish(app)
            gameMode_checkCollisionSuper(app)
    

        else:
            if app.buySuper:
                app.buySuper=not app.buySuper
            app.setSuper=False
            app.setTypicalFish=True
            if app.timePassed%100==0:
                gameMode_shootFish(app)
            gameMode_moveFish(app)
            gameMode_checkCollision(app)#########check colission
        gameMode_checkEnemy(app)

        ######for dog to shoot bullet back to cats
        if 10000<=app.timePassed<=200000:
            l=len(app.doglist)
            for i in range(0,l,3):
                dog=app.doglist[i]
                x,y=dog.x,dog.y

                if app.timePassed%1000==0:
                    speed=dog.dy
                    new=Enemy(x,y,None,speed) ##dog's bullets
                    app.dogBullet.append(new)
                
            for dogBullet in app.dogBullet:
                    dogBullet.moveEnemyBullet()
                    if dogBullet.y>700:
                        app.dogBullet.remove(dogBullet)
                        
        
        gameMode_checkDogBulletHit(app)
       

    
def gameMode_drawSuperFish(app,canvas):
    if not app.pause and not app.endGame:
        for superfish in app.superFish:
            leftx,lefty=superfish.leftx, superfish.lefty
            rightx, righty=superfish.rightx, superfish.righty
            dr=10
            x,y=superfish.x, superfish.y
            canvas.create_oval(leftx-dr,lefty-dr,leftx+dr,lefty+dr,\
                            fill='yellow')
            canvas.create_oval(x-dr,y-dr,x+dr,y+dr,fill='orange')
            canvas.create_oval(rightx-dr,righty-dr,rightx+dr,righty+dr,fill='blue')
       
def gameMode_dropDog(app):
    if not app.pause and not app.endGame:
    
            num1=random.randint(1,8)
            speed=num1*10
            new=Enemy(random.randint(10,530),20,app.health,speed)
            app.doglist.append(new)
        

def buyPage(app,canvas):
    
    x,y=app.width//2,app.height//2
    canvas.create_rectangle(x-200,y-150,x+200,y+150,fill='SteelBlue1',outline='SteelBlue1')
    canvas.create_rectangle(x-50,y+50,x+50,y+90,fill='',outline='black',width=6)
    canvas.create_text(x,y+70, text='BUY',fill='black',font='Impact 22 ')
    canvas.create_text(x,y-100, text='Buy Super Bullet Time +1',font='Impact 24 ',fill='black')
    canvas.create_text(x,y-50, text='Buy Path Finding Bullets +1',font='Impact 24',fill='black')



def gameMode_drawDog(app,canvas):
    if not app.pause and not app.endGame:
        for dog in app.doglist:
            health=dog.health
            
            x,y=dog.x,dog.y
            canvas.create_image(x,y, image=app.imagedog)
            canvas.create_text(x,y-5, text=f'{health}', fill='firebrick1',font='Helvetica 14 bold italic')


def gameMode_moveDog(app):
    if not app.pause and not app.endGame:
        for dog in app.doglist:
            dog.falling()
    


def gameMode_findPathFindFish(app,bullet):
    if not app.pause and not app.endGame:
        best=1000
        bestDog=None
        for dog in app.doglist:
            curr= bullet.findEnemy(dog)
            if curr<best:
                best=curr
                bestDog=dog
        return bestDog
########################
def gameMode_shootPathFindFish(app):
    if not app.pause and not app.endGame and app.setPathFind:
        x,y=app.cat.x,app.cat.y
        pfFish=PathFindBullet(x,y)
        app.pathFindBullet.append(pfFish)


def gameMode_movePathFindFish(app,target):###target is a enemy class object
    if not app.pause and not app.endGame and app.setPathFind:
        for pfFish in app.pathFindBullet:
            pfFish.moveTowards(target)

def checkPathFindCollision(app,target):
    if not app.pause and not app.endGame:
        if len(app.pathFindBullet)>0:
            pfFish=app.pathFindBullet[0]
           
            
            if pfFish.hitEnemy(target) and target in app.doglist:
                app.drawPathFind=False
                app.setPathFind=False
                app.doglist.remove(target)
            if target not in app.doglist:
                app.drawPathFind=False
                app.setPathFind=False
                app.setPathFind+=1
             
########################

def gameMode_shootSuperFish(app):
    if not app.pause and not app.endGame:
        x,y=app.cat.x,app.cat.y
        superFish=SuperBullet(x,y)
        app.superFish.append(superFish)


def gameMode_moveSuperFish(app):
    if not app.pause and not app.endGame:
        for superfish in app.superFish:
            if (superfish.x, superfish.y)!=(app.cat.x,app.cat.y):
                superfish.moveBack(app.cat.x)
            superfish.move()
            if superfish.lefty<0:
                app.superFish.remove(superfish)

def gameMode_shootFish(app):
    if not app.pause and not app.endGame and app.setTypicalFish:
        x,y=app.cat.x,app.cat.y
        newFish=Bullet(x,y)
        app.fishList.append(newFish)
def gameMode_drawFish(app,canvas):
    if not app.pause and not app.endGame:
        for fish in app.fishList:
            x,y=fish.x,fish.y
            canvas.create_oval(x-5,y-5, x+5, y+5,fill='black') ## a circle for fish so far
def gameMode_moveFish(app):
    if not app.pause and not app.endGame and app.setTypicalFish:
        for fish in app.fishList:
            if (fish.x,fish.y)!=(app.cat.x,app.cat.y):
                fish.moveBack(app.cat.x)
            fish.moveBullet()########
            if fish.y<0:
                app.fishList.remove(fish)
  
def gameMode_drawCatHealth(app,canvas):
    x,y=app.cat.x,app.cat.y
    canvas.create_text(x,y-25,text=f'{app.catHealth}',font='Times 18 bold italic',fill='red')


def gameMode_checkCollisionSuper(app):
    if app.setSuper:
        for superfish in app.superFish:
            for dog in app.doglist:
                if superfish.hitEnemy(dog):
                    if superfish in app.superFish:
                        app.superFish.remove(superfish)
                    app.score+=10
                    # print('you score')
                    dog.health-=50
                    if dog.health<=0:
                        app.doglist.remove(dog)


def gameMode_checkCollision(app):
    for fish in app.fishList:
        for dog in app.doglist:
        
            if fish.hitEnemy(dog):

                if fish in app.fishList:
                    app.fishList.remove(fish)
                app.score+=10
                dog.reduceHealth()
                if dog.health<=0:
                    app.doglist.remove(dog)


def gameMode_checkDogBulletHit(app):
    ###check whether the green rectangles hit cat or not
    for dogBullet in app.dogBullet:
        dogx,dogy=dogBullet.x, dogBullet.y
        catx,caty=app.cat.x,app.cat.y
        if catx-50<=dogx<=catx+50 and caty-50<=dogy<=caty+50:
            app.catHealth-=50
            app.dogBullet.remove(dogBullet)

def gameMode_checkEnemy(app):
    for dog in app.doglist:
        if dog.hitGround() or app.catHealth<=0:
            
            app.endGame=True
            app.scoreList.append(app.score)
            app.mode='endGameMode'
            
        
def endGameMode_redrawAll(app, canvas):
    font='Times 28 bold'
    canvas.create_image(app.width//2,app.height//2,image=app.historyUI)
    canvas.create_text(app.width//2, app.height//4, text=f'You Score {app.score}!',font=font)
    canvas.create_rectangle(app.width//2-50, app.height//2-30, app.width//2+50,\
        app.height//2+30, fill='yellow3',width=5)
    canvas.create_text(app.width//2, app.height//3, text='Press r to Return Home',font=font)
    canvas.create_text(app.width//2, app.height//2, text='Play Again',font='Times 20 bold')



def endGameMode_mousePressed(app, event):
    if app.width//2-50<=event.x<=app.width//2+50 \
        and app.height//2-30<=event.y<=app.height//2+30:
        app.scoreList.append(app.score)
        app.mode='gameMode'
        reset(app)
def endGameMode_keyPressed(app,event):
    if event.key=='r':
        app.mode='startPageMode'


def cannotAfford(app,canvas):
    x,y=app.width//2,app.height//2
    canvas.create_rectangle(x-200,y-150,x+200,y+150,fill='SteelBlue1',outline='SteelBlue1')
    canvas.create_rectangle(x-80,y+50,x+80,y+90,fill='',outline='black',width=5)
    canvas.create_text(x,y+70, text='Not Enough to buy',fill='black',font='Impact 22')
    canvas.create_text(x,y-100, text='Buy Super Bullet Time +1',font='Impact 24',fill='black')
    canvas.create_text(x,y-50, text='Buy Path Finding Bullets +2',font='Impact 24',fill='black')

def gameMode_mousePressed(app,event):
    x,y=app.width//2,app.height//2
    if 530<=event.x<=570 and 30<=event.y<=70:
        app.wantToBuy=True
        app.pause=True

    if app.wantToBuy and x-50<=event.x<=x+50 and y+50<=event.y<=y+90:
        if app.score>=150:
            app.score-=150
            app.pathFindTimes+=1
            app.superTime=0
            app.wantToBuy=False
            app.pause=False
            app.buySuper=True
            app.setSuper=True
        
        else:
            app.wantToBuy=False
            app.pause=False
            # app.setTypical

        


def gameMode_keyReleased(app,event):
    if not app.pause:
        if event.key=='w':
        
            app.cat.y-=app.cat.dx
            if app.cat.y<350:
                app.cat.y+=app.cat.dx
        elif event.key=='a':
            app.cat.x-=app.cat.dx
            if app.cat.x<20:
                app.cat.x+=app.cat.dx
        elif event.key=='s':
            app.cat.y+=app.cat.dx
            if app.cat.y>650:
                app.cat.y-=app.cat.dx
        elif event.key=='d':
            app.cat.x+=app.cat.dx
            if app.cat.x>580:
                app.cat.x-=app.cat.dx
        elif event.key=='p' and not app.wantToBuy:
            app.pause=not app.pause
        # if event.key=='w':
        #     app.cat.y-=
        # elif event.key=='a':
        #     app.cat.moveLeft()
        # elif event.key=='s':
        #     app.cat.moveDown()
        # elif event.key=='d':
        #     app.cat.moveRight()
        # elif event.key=='p':
        #     app.pause=not app.pause
    else:
        
        if event.key=='p':
            app.pause=not app.pause
#     

def gameMode_keyPressed(app,event):
    if not app.pause:
        if event.key=='j' and not app.setSuper and app.pathFindTimes>0 and len(app.doglist)>0: #### shoot path-finding 
            #########
            #set Path Finding Bullet
            #########
            app.setPathFind=True
            app.drawPathFind=True
            app.pathFindBullet=[]
            x,y=app.cat.x,app.cat.y
            app.pathBullet=PathFindBullet(x,y)
            app.target=gameMode_findPathFindFish(app,app.pathBullet)
          

            ###########################
            app.pathFindTimes-=1
        
    if event.key=='r':
                app.mode='startPageMode'
                app.scoreList.append(app.score)

def reset(app):
    app.score = 0
    app.endGame=False
    app.pause=False
    app.wantToBuy=False
    
    app.buySuper=False

    app.fishList=[]
    app.setTypicalFish=True
    app.superFish=[]
    app.setSuper=False
    app.superTime=0

    app.pathFindBullet=[]
    app.setPathFind=False
    app.target=None
    app.pathFindTimes=6
    app.drawPathFind=False

    app.health=50
    app.catHealth=500

    app.cat=Player(600,650) 
    app.dog=Enemy(random.randint(10,580),20,app.health,40)
    app.doglist=[app.dog]

    app.dogBullet=[]
    app.timePassed=0
##########################################
# Main 
##########################################


def appStarted(app):
    app.mode = 'startPageMode'
    app.score = 0

    app.timerDelay = 50
    #### all images are imported from my own camera roll
    app.image1 = app.loadImage('dog.png')
    app.imagedog = ImageTk.PhotoImage(app.scaleImage(app.image1, 1/3))
    app.image2 = app.loadImage('cat_mid.png')
    app.imagecat = ImageTk.PhotoImage(app.scaleImage(app.image2, 1/4))

    app.buyButton=ImageTk.PhotoImage(app.scaleImage(app.loadImage('buyButton.png'),1/4))
    app.fishBullet=ImageTk.PhotoImage(app.scaleImage(app.loadImage('fishBullet.png'),1/2))
    app.arrows=ImageTk.PhotoImage(app.scaleImage(app.loadImage('arrows.png'),1/2))
    ########
    #https://www.istockphoto.com/photos/cartoon-dog-bone
    app.bone=ImageTk.PhotoImage(app.scaleImage(app.loadImage('bone.png'),1/2))
    ##########
    app.bone2=ImageTk.PhotoImage(app.scaleImage(app.loadImage('bone copy.png'),1/3))
    app.introCat=ImageTk.PhotoImage(app.scaleImage(app.loadImage('introPage.png'),1/2))
    app.introcat2=ImageTk.PhotoImage(app.scaleImage(app.loadImage('introcat2.png'),1/3))
    
    app.endGame=False
    app.pause=False

    app.scoreList=[]

    app.shopLocation=[]

    app.wantToBuy=False
    
    app.buySuper=False
    #####FISH/BULLET
   
    app.fishList=[]
    app.setTypicalFish=True
    app.superFish=[]
    app.setSuper=False
    app.superTime=0

    app.pathFindBullet=[]
    app.setPathFind=False
    app.target=None
    app.pathFindTimes=6
    app.drawPathFind=False

    app.health=50
    app.catHealth=500

    app.cat=Player(600,650)
    app.dog=Enemy(random.randint(10,580),20,app.health,40)
    app.doglist=[app.dog]

    app.dogBullet=[]
    app.timePassed=0

    app.x=0
    app.y=0

    ####### SCORE PAGE
    app.historyUI=ImageTk.PhotoImage(app.scaleImage(app.loadImage('historyScore.jpg'),0.6))

    app.spritePhotoImages = loadAnimatedGif('sample-animatedGif.gif')
  
    app.spriteCounter = 0
##########citations:
#https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#loadImageUsingUrl:~:text=Copy-,Animated,-Gifs
def loadAnimatedGif(path):
    # load first sprite outside of try/except to raise file-related exceptions
    spritePhotoImages = [ PhotoImage(file=path, format='gif -index 0') ]
   
    i = 1
    while True:
        try:
            spritePhotoImages.append(PhotoImage(file=path,
                                                format=f'gif -index {i}'))
            i += 1
        except Exception as e:
            return spritePhotoImages
#############
def startPageMode_redrawAll(app, canvas):
    font = 'Noteworthy 26 bold'
    canvas.create_rectangle(0,0,650,750,fill='LightBlue1')    
    canvas.create_image(600,900,image=app.arrows)
    canvas.create_image(app.x,app.y,image=app.bone)
    canvas.create_image(app.x,app.y+400,image=app.bone2)
    canvas.create_text(app.width/2, 180, text='C a t / D o g  W A R :)',font=font,\
                    fill='SlateBlue1')
    canvas.create_text(app.width/2, 250, text='1.INTRODUCTION',
                    font=font, fill='black')
    canvas.create_text(app.width/2, 330, text='2.PLAY GAME',
                       font=font, fill='black')
    canvas.create_text(app.width/2, 410, text='3.HISTORY SCORES',
                       font=font, fill='black')
    
def startPageMode_timerFired(app):
    app.timePassed+=50
    if app.timePassed%100==0:
        x,y=random.randint(1,2),2 
        app.x,app.y=x*100,y*100
    
def startPageMode_keyPressed(app, event):
    if event.key=='1':
        app.mode='introMode'
    elif event.key=='2':
        app.mode = 'gameMode'
        reset(app)
    elif event.key=='3':
        app.mode = 'historyScoreMode'
  
##########################################
# Intro Mode
def introMode_redrawAll(app,canvas):
    font = 'Times 18 bold'
    tex='Help my cat beat my naughty\n dog who always attacks her!!'
    canvas.create_text(app.width/2+100, app.height//5,text=tex, fill='cyan2',font='Times 20 bold')
    textIntro='PLZ DO NOT RESIZE :).Let it be 600*700\nPress w,a,s,d to control the cat\npress j to shoot the pathfinding bullet(limited numbers of time)\nAt certain time you will get a more powerful bullet than the default one\nEach time the cat gets hit by the dog bullet,she will lose 100 health\nYou can also click the Buy Button to get Super Bulelts'
    t=canvas.create_text(app.width/2+20, app.height//2-80, text=textIntro, font=font)
  
    canvas.create_image(550,150,image=app.introCat)
    photoImage = app.spritePhotoImages[app.spriteCounter]
    canvas.create_image(300, 500, image=photoImage)
    
def introMode_timerFired(app):
    app.spriteCounter = (1 + app.spriteCounter) % len(app.spritePhotoImages)

def introMode_keyPressed(app,event):
    if event.key=='r':
        app.mode='startPageMode'

##########################################
# History Score
##########################################
def historyScoreMode_redrawAll(app,canvas):
    font = 'Impact 50 '
    canvas.create_image(app.width//2,app.height//2,image=app.historyUI)
    canvas.create_text(app.width//2,100, text='Score Log',\
        font=font,fill='RoyalBlue1')
    historyScoreMode_displayScore(app,canvas)

def historyScoreMode_getTextLoc(ystart,i):
    dy=50
    return ystart+i*dy
def historyScoreMode_timerFired(app):
    l=len(app.scoreList)
    if l>10:####keep the score for this round
        app.scoreList=app.scoreList[l-10:]
     

def historyScoreMode_displayScore(app,canvas):
    font = 'Impact 26'
    ystart=150
    for i in range(len(app.scoreList)):
        y=historyScoreMode_getTextLoc(ystart,i)
        canvas.create_text(app.width//2,y, text=f'{i+1}.score {app.scoreList[i]}', \
            font=font,fill='black')
######will only display the latest 10 scores
def historyScoreMode_keyPressed(app,event):
    if event.key=='r':
        app.mode='startPageMode'
runApp(width=600, height=700)