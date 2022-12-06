import json
from collections import defaultdict
from CheckRules import CheckRules

class CheckHeuristic():
    @staticmethod
    # TODO: change possible moves here to full possible move (currently is playable area)
    def getPatternDict(bot_game, player, opponent, debug=False): 
        forbidden_moves = bot_game.forbidden_moves[player]
        patterns = list()
        string_len, low, high = 7, -3, 4
        isOutsideBoard = lambda x, y: x < 0 or y < 0 or x >= bot_game.goban_size or y >= bot_game.goban_size or (x, y) in forbidden_moves
        stone_list = bot_game.stone_list
        captures = bot_game.player_captures[player]

        for x, y in stone_list[player]:
            c1 = ['_'] * string_len
            c2 = ['_'] * string_len
            c3 = ['_'] * string_len
            c4 = ['_'] * string_len

            for i in range(low, high):
                ## get_line pattern
                coord = (x + i, y)
                if coord in stone_list[player]:
                    c1[i-low] = 'X'
                elif coord in stone_list[opponent]:
                    c1[i-low] = 'O'
                elif isOutsideBoard(*coord):
                    c1[i-low] = '.'

                ## get column patter
                coord = (x, y + i)
                if coord in stone_list[player]:
                    c2[i-low] = 'X'
                elif coord in stone_list[opponent]:
                    c2[i-low] = 'O'
                elif isOutsideBoard(*coord):
                    c2[i-low] = '.'

                ## get left diagonal pattern
                coord = (x + i, y + i)
                if coord in stone_list[player]:
                    c3[i-low] = 'X'
                elif coord in stone_list[opponent]:
                    c3[i-low] = 'O'
                elif isOutsideBoard(*coord):
                    c3[i-low] = '.'

                ## get right diagonal pattern
                coord = (x - i, y + i)
                if coord in stone_list[player]:
                    c4[i-low] = 'X'
                elif coord in stone_list[opponent]:
                    c4[i-low] = 'O'
                elif isOutsideBoard(*coord):
                    c4[i-low] = '.'

            captures += sum('XOOX' in elem for elem in (c1, c2, c3, c4)) * 2
            patterns.append(''.join(c1))
            patterns.append(''.join(c2))
            patterns.append(''.join(c3))
            patterns.append(''.join(c4))

        dic = defaultdict(int)
        dic['captures'] = captures


        def _countPattern(dic, patterns):
            fiveInRowSet = {'XXXXXXX', '_XXXXX_', 'OXXXXXO', '_XXXXXO', 'XXXXXXO', 'OXXXXXX', 'OXXXXX_', '_XXXXXX', 'XXXXXX_'}
            liveFourSet = {'X_XXXXX', '_X_XXXO', 'OX_XXXX', 'XXX_X_X', '_OXX_XX', 'XX_XXO_', 'X_XX_XX', 'XOX_XXX', '_OX_XXX',
                            '_X_XXXX', 'X_XXXXO', 'X_XXX_O', '_X_XXX_', 'XXXXX_X', '__XXXX_', 'OXXXX_X', '__X_XXX', 'XX_XX_X',
                            'XXX_XX_', 'XX_XX__', 'XX_XX_O', 'OXXX_XX', 'XOXXX_X', 'XXX_XO_', '_XXXX__', 'OX_XXXO', 'X_XXXOO',
                            'XXXX_XO', 'XXX_X_O', 'XOXX_XX', 'XXX_XOX', 'XXX_XOO', 'XXXX_X_', 'XXX_XXO', 'OX_XXX_', 'X_X_XXX',
                            '_XXX_XX', '_XX_XX_', 'XXX_XXX', 'XXXX_XX', 'XX_XXX_', 'X_XXXO_', 'X_XXX__', 'OOXX_XX', 'XXX_X__',
                            'XX_XXOO', 'OXX_XXO', '_XX_XXX', '_XXX_X_', 'O_XXX_X', 'OXX_XXX', 'XX_XXXO', 'X_XXX_X', 'X_XXXOX',
                            'X_XXXX_', '_XXXX_X', 'XX_XXXX', '__XX_XX', 'OXX_XX_', 'XX_XXOX', 'OOX_XXX', 'O_XXXX_', 'O_X_XXX',
                            'OOXXX_X', '_XXX_XO', 'OXXX_XO', '__XXX_X', '_OXXX_X', 'O_XX_XX', '_XXXX_O', 'OXXX_X_', '_XX_XXO'}

            deadFourSet = {'OXXXX__', 'OXXXX_O', 'OXXXX_X', '_OXXXX_', 'OOXXXX_', 'XOXXXX_'}
            deadThreeSet = {'OXXX__X', 'OXXX__O', 'OXXX___', '_OXXX__', 'OOXXX__', 'XOXXX__', '___XXXO', 'X__XXXO', 'O__XXXO',
                            '__XXXO_', '__XXXOO', '__XXXOX', 'OXX_X_O', 'OXX_X_X', 'OXX_X__', '_OXX_X_', 'OOXX_X_', 'XOXX_X_',
                            'O_X_XXO', 'X_X_XXO', '__X_XXO', '_X_XXO_', '_X_XXOO', '_X_XXOX', 'OOX_XX_', 'XOX_XX_', '_OX_XX_',
                            'OX_XX_O', 'OX_XX_X', 'OX_XX__', 'O_XX_XO', 'X_XX_XO', '__XX_XO', '_XX_XOO', '_XX_XOX', '_XX_XO_',
                            'O_XXX_O'}
            liveThreeSet = {'_O_XXX_', 'OOXX_X_', 'XX_XX_O', '_OX_XX_', '_X_X_X_', '_X_XXOO', '__XX__X', '_X_XXO_', '__X_XXO',
                            'X_X_X_X', 'X_XX___', '___XX_X', '__XX_X_', 'OO_X_XX', 'X_X_XOX', 'OX_XX_O', '___X_XX', '_X_XX__',
                            'O_XXX_O', '_XXX___', 'XO_XXX_', 'X_XX_XX', 'O_XXX__', 'XO_X_XX', 'XX_X_X_', '_X_XXXO', 'XX_XX_X',
                            'X_XXX_X', 'X_X_XXO', 'X_X_X_O', 'X_X_XO_', 'X_XX_X_', 'O_X_XXO', 'XOXX_X_', '_XXX_OO', '_XX_XXO',
                            'X__XXX_', 'O_XX_XX', '_XX_X_O', '__XX_XX', '_XX_XO_', 'X_X_XX_', 'OXX_X_O', 'XX_X__O', 'OX_XX__',
                            'OOX_X_X', '_XX_XOO', '_O_X_XX', '__XXX__', 'XX_X__X', '_XXX_O_', 'OXXX_X_', '_X_X_XO', '_XXX_OX',
                            'O_X_XXX', '_XX_XX_', 'OX_X_XX', '_XXX_X_', 'XX_XX__', '__XXX_X', '_X_XXXX', 'O_XXX_X', 'X_XXX_O',
                            '_XX_XXX', 'XOX_XX_', 'XOX_X_X', 'O_XX_X_', 'X__XX_O', 'O__XXX_', 'XX_XXX_', 'X_XX_XO', 'OX_X_X_',
                            '_XX__X_', '_XX_X_X', '_OXX_X_', '___XXX_', '_XXX__O', 'X_XX_OO', '_X_X_XX', 'XX_X_XX', '_O_XX_X',
                            '_XXX_XX', 'X_X_XXX', 'X_X_XOO', 'OX__XX_', '_X_XXX_', 'XX_X_OO', '_XXX__X', '_XX_X__', 'X_XX_OX',
                            '_XX_XOX', 'O_X_X_X', 'XX_X___', 'O_XX__X', 'X_XX__O', 'XXX_X_X', '_X_XX_O', '_X_XX_X', 'XXX_X_O',
                            'X_XXX__', 'OXX_X__', '_X_XXOX', 'XXX_X__', 'O_X_XX_', 'OXX_X_X', 'O_XX_XO', 'X_XX_O_', 'OX_X_XO',
                            'OO_XXX_', 'OX_XXX_', 'XX_X_XO', 'XX_X_OX', 'XO_XX_X', 'X__XX_X', '__XX_XO', '_X__XX_', 'O__X_XX',
                            '_OX_X_X', 'XXXX_X_', 'XXX_XX_', 'O__XX_X', 'X__X_XX', 'OXX_XX_', 'XX__XX_', 'OOX_XX_', '_XX__XX',
                            'X_XX__X', '__X_X_X', 'XX_X_O_', '__X_XX_', 'OO_XX_X', '_XXX_XO', '__XXX_O', '_XX__XO', 'X__XX__',
                            '__X_XXX', 'X_X_X__', 'OX_XX_X'}
            deadTwoSet = {'OX__X__', 'OX__X_O', 'OX__X_X', '_OX__X_', 'OOX__X_', 'XOX__X_', '_X__XO_', '_X__XOO', '_X__XOX',
                           '__X__XO', 'O_X__XO', 'X_X__XO', 'OX_X___', 'OX_X__O', 'OX_X__X', '_OX_X__', 'OOX_X__', 'XOX_X__',
                           '__X_XO_', '__X_XOO', '__X_XOX', '___X_XO', 'O__X_XO', 'X__X_XO', 'OXX____', 'OXX___O', 'OXX___X',
                           '_OXX___', 'OOXX___', 'XOXX___', '___XXO_', '___XXOO', '___XXOX', '____XXO', 'O___XXO', 'X___XXO'}
            liveTwoSet = {'_X___X_', '_X___XO', '_X___XX', 'OX___X_', 'OX___XO', 'OX___XX', 'XX___X_', 'XX___XO', 'XX___XX',
                           'X___X__', 'X___X_O', 'X___X_X', 'X___XO_', 'X___XOO', 'X___XOX', 'X___XX_', 'X___XXO', 'X___XXX',
                           '__X___X', '_OX___X', '_XX___X', 'O_X___X', 'OOX___X', 'OXX___X', 'X_X___X', 'XOX___X', 'XXX___X',
                           '_X__X__', '_X__X_O', '_X__X_X', 'OX__X__', 'OX__X_O', 'OX__X_X', 'XX__X__', 'XX__X_O', 'XX__X_X',
                           'X__X___', 'X__X__O', 'X__X__X', 'X__X_O_', 'X__X_OO', 'X__X_OX', 'X__X_X_', 'X__X_XO', 'X__X_XX',
                           '__X__X_', '_OX__X_', '_XX__X_', 'O_X__X_', 'OOX__X_', 'OXX__X_', 'X_X__X_', 'XOX__X_', 'XXX__X_',
                           '__X__X_', '__X__XO', '__X__XX', 'O_X__X_', 'O_X__XO', 'O_X__XX', 'X_X__X_', 'X_X__XO', 'X_X__XX',
                           '_X__X__', '_X__X_O', '_X__X_X', '_X__XO_', '_X__XOO', '_X__XOX', '_X__XX_', '_X__XXO', '_X__XXX',
                           '___X__X', '_O_X__X', '_X_X__X', 'O__X__X', 'OO_X__X', 'OX_X__X', 'X__X__X', 'XO_X__X', 'XX_X__X',
                           '__X_X__', '__X_X_O', '__X_X_X', 'O_X_X__', 'O_X_X_O', 'O_X_X_X', 'X_X_X__', 'X_X_X_O', 'X_X_X_X',
                           '_X_X___', '_X_X__O', '_X_X__X', '_X_X_O_', '_X_X_OO', '_X_X_OX', '_X_X_X_', '_X_X_XO', '_X_X_XX',
                           '___X_X_', '_O_X_X_', '_X_X_X_', 'O__X_X_', 'OO_X_X_', 'OX_X_X_', 'X__X_X_', 'XO_X_X_', 'XX_X_X_',
                           '__XX___', '__XX__O', '__XX__X', '___XX__', 'O__XX__', 'X__XX__'}
            uselessOneSet = {'___X___', '___X__O', '___X__X', 'O__X___', 'O__X__O', 'O__X__X', 'X__X___', 'X__X__O', 'X__X__X',
                             '__X____', '__X___O', '__X___X', '__X__O_', '__X__OO', '__X__OX', '__X__X_', '__X__XO', '__X__XX',
                             '____X__', '_O__X__', '_X__X__', 'O___X__', 'OO__X__', 'OX__X__', 'X___X__', 'XO__X__', 'XX__X__'}

            if debug:
                print(patterns)
            for pattern in patterns:
                if pattern in fiveInRowSet:
                    dic["fiveInRow"] += 1
                elif pattern in deadFourSet:
                    dic["deadFour"] += 1
                elif pattern in liveFourSet:
                    dic["liveFour"] += 1
                elif pattern in deadThreeSet:
                    dic["deadThree"] += 1
                elif pattern in liveThreeSet:
                    dic["liveThree"] += 1
                elif pattern in deadTwoSet:
                    dic["deadTwo"] += 1
                elif pattern in liveTwoSet:
                    dic["liveTwo"] += 1
                elif pattern in uselessOneSet:
                    dic["uselessOne"] += 1

        _countPattern(dic, patterns)

        return dic

