def mpclop():
    colors=['Red','Blue','Green']
    states=['Andhra','Karnataka','TamilNadu','Kerala']
    neighbours={'Andhra':['Karnataka','TamilNadu'],'Karnataka':['Andhra','TamilNadu','Kerala'],'TamilNadu':['Andhra','Karnataka','Kerala'],'Kerala':['Karnataka','TamilNadu']}
    colors_of_state={}
    def coloring(state,color):
        for neighbour in neighbours.get(state):
            color_of_neighbour=colors_of_state.get(neighbour)
            if color_of_neighbour==color:
                return False
        return True
    def get_color_for_state(state):
        for color in colors:
            if coloring(state,color):
                return color
    def main():
        for state in states:
            colors_of_state[state]=get_color_for_state(state)
            print(colors_of_state)
    main()
def mpcl():
    print('''colors=['Red','Blue','Green']
states=['Andhra','Karnataka','TamilNadu','Kerala']
neighbours={'Andhra':['Karnataka','TamilNadu'],'Karnataka':['Andhra','TamilNadu','Kerala'],'TamilNadu':['Andhra','Karnataka','Kerala'],'Kerala':['Karnataka','TamilNadu']}
colors_of_state={}
def coloring(state,color):
    for neighbour in neighbours.get(state):
        color_of_neighbour=colors_of_state.get(neighbour)
        if color_of_neighbour==color:
            return False
    return True
def get_color_for_state(state):
    for color in colors:
        if coloring(state,color):
            return color
def main():
    for state in states:
        colors_of_state[state]=get_color_for_state(state)
        print(colors_of_state)
main()
''')