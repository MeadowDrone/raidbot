def guides(instr):
    text = instr[6:]
    alex = ['that\'s not a raid number, silly',
                'https://www.youtube.com/watch?v=ldtNxxoVH5M', 
                'xeno: https://www.youtube.com/watch?v=ooNCi_9VL3Y&feature=youtu.be \nmtq: https://www.youtube.com/watch?v=XSstMu3f9d4 \ntext: http://www.dtguilds.com/forum/m/6563292/viewthread/23552103-alexander-gordia-savage-a2s-cuff-father-strategy-guide' , 
                'mtq: https://www.youtube.com/watch?v=2HLnZIZwRhQ \ntext: http://www.dtguilds.com/forum/m/6563292/viewthread/23022915-alexander-gordia-normal-arm-father-a3-strategy-guide', 
                'mrhappy:\nhttps://www.youtube.com/watch?v=zkbOdAYNrDg']
    turns = ['that\'s not a turn, silly', 'https://www.youtube.com/watch?v=ZIoyLNYyOzo', 'https://www.youtube.com/watch?v=mqP2ooPB9ys',
                'https://www.youtube.com/watch?v=BdT2BFEX4I8', 'https://www.youtube.com/watch?v=pb_hDiiBOi4', 
                'https://www.youtube.com/watch?v=1fsPp9IQXuc', 'https://www.youtube.com/watch?v=HVqe6D9UlkQ', 
                'https://www.youtube.com/watch?v=zlFDCI-c9wE', 'https://www.youtube.com/watch?v=IeUiwRI6rqM', 
                'https://www.youtube.com/watch?v=K_lnPoQNu7w', 'https://www.youtube.com/watch?v=9qBV21L37E0', 
                'https://www.youtube.com/watch?v=3HRe4bLjpNk', 'https://www.youtube.com/watch?v=d0zqDdg9zm4',
                'https://www.youtube.com/watch?v=Fbmd4eRNwnE']
    
    if 'turn' in instr:
        try:
            int(text)
            isInt = True
            
        except:
            isInt = False
            bot.sendMessage(chat_id=chat_id,
                    text='you need to enter a turn number as an argument. eg: /turn 5')

        if (isInt):
            arg = int(text)
            if arg < 0:
                return 'that\'s not a coil turn, silly'
            elif arg > 13:
                return 'that\'s not a coil turn, silly'
            else:
                return ('turn %s guide:\n%s' % (str(arg), turns[arg]))
    elif 'alex' in instr:
        try:
            int(text)
            isInt = True
        except:
            isInt = False
            return 'you need to enter a number as an argument. eg: /alex 1'

        if (isInt):
            arg = int(text)
            if arg < 0:
                return 'that\'s not an alex savage raid, silly'
            elif arg > 4:
                return 'getting a bit ahead of yourself, aren\'t you?'
            else:
                return ('alexander (savage) %s guide:\n%s' % (str(arg), alex[arg]))