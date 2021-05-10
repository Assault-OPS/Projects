from string import ascii_uppercase as ass

asci = [ ' #  ##   ## ##  ### ###  ## # # ###  ## # # #   # # ###  #  ##   #  ##   ## ### # # # # # # # # # # ###    ',
		 '# # # # #   # # #   #   #   # #  #    # # # #   ### # # # # # # # # # # #    #  # # # # # # # # # #   #    ',
		 '### ##  #   # # ##  ##  # # ###  #    # ##  #   # # # # # # ##  # # ##   #   #  # # # # # #  #   #   #     ',
		 '# # # # #   # # #   #   # # # #  #  # # # # #   # # # # # # #    ## # #   #  #  # # # # ### # #  #  #      ',
		 '# # ##   ## ##  ### #    ## # # ###  #  # # ### # # # #  #  #     # # # ##   #  ###  #  # # # #  #  ###    ']
alpha = { a:b*4 for a,b in zip([b for b in ass], range(len(ass)))}
alpha[' '] = 104
while True:
    t = input('> ').upper()
    print('\n'.join(''.join(i[alpha[a]:alpha[a]+4] for a in t if a in alpha) for i in asci))
