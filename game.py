#!/usr/bin/python
#
# Copyright 2015 - Jonathan Gordon
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This software is distributed on an "AS IS" basis, WITHOUT WARRANTY OF ANY
# KIND, either express or implied.

import random

from common import *
from cards import helpers
from players import *
import logger

def init_games():
	global __all_cards
	global __all_wonders

	__all_cards = helpers.read_cards_file("card-descriptions.txt")
	__all_wonders = Wonders.read_wonders_file("wonders.txt")

class GameState:
	def __init__(self, players):

		self.player_count = len(players)
		self.players = []
		self.ages = []
		self.decks = [[]] * len(players)
		self.discard_pile = []
		self.logger = logger.Logger()
		for i in range(len(players)):
			name, persona = players[i]
			self.players.append(Players.Player(name))
			self.players[i].set_personality(persona())
		
	def setup_age_cards(self, cards):
		age_1 = [c for c in cards if c.age == 1 and c.players <= self.player_count]
		age_2 = [c for c in cards if c.age == 2 and c.players <= self.player_count]
		age_3 = [c for c in cards if c.age == 3 and c.get_colour() != CARDS_PURPLE and c.players <= self.player_count]
		purple = [c for c in cards if c.age == 3 and c.get_colour() == CARDS_PURPLE and c.players <= self.player_count]

		random.shuffle(age_1)
		random.shuffle(age_2)
		random.shuffle(purple)
		age_3 += purple[0 : self.player_count + 2]
		random.shuffle(age_3)
		
		self.ages = [age_1, age_2, age_3]
	
	def deal_wonders(self, wonders):
		# print(wonders)
		# input()
		random.shuffle(wonders)
		for i in range(self.player_count):
			self.players[i].wonder = wonders[i]
			self.players[i].side_wonder_a = random.choice([True, False])
			# print(self.players[i].side_wonder_a)
			# print(1)
			# print(random.choice([True, False]))
			# print(2)
			# input()
		# print(self.players[1].wonder)
		# input()


	def deal_age_cards(self, age):
		cards = self.ages[age][0:]
		p = 0
		for i in range(self.player_count):
			self.decks[i] = []
		while len(cards):
			self.decks[p].append(cards[0])
			p += 1
			p %= self.player_count
			cards = cards[1:]
	
	def _get_west_player(self, playerid):
		return self.players[(playerid + self.player_count - 1) % self.player_count]

	def _get_east_player(self, playerid):
		return self.players[(playerid + 1) % self.player_count]
	
	def play_turn(self, offset):
		for i in range(self.player_count):
			player = self.players[i]
			west_player = self._get_west_player(i)
			east_player = self._get_east_player(i)
			deckid = (i + offset) % self.player_count
			# input(1)
			player.print_tableau()
			# input("pause")
			# This loop is actually wrong.
			# Everyone should choose the card they will play, server
			# validates the move is legal, then each player plays the card
			# Then each player adds the new card to their tableau
			# action, card = can_buy_card(self.decks[deckid], west_player, east_player)
			action, card = player.play_hand(self.decks[deckid], west_player, east_player) #action c'est le numéro de l'action (entre 0 et 2) et card la carte 
			
			# print(action)
			# print(card)
			# input(2)
			if action == ACTION_PLAYCARD:
				player.play_card(card, west_player, east_player)
			elif action == ACTION_DISCARD:
				self.discard_pile.append(card)
				player.money += 3
			elif action == ACTION_STAGEWONDER:
				raise NotImplementedError
				# make sure we can do that
			# 	input("pause1")
			# input("pause2")
			self.decks[deckid].remove(card)
			
	
	def game_loop(self):
		print("beginning of the game")
		for age in range(3):
			print(f"Age {age+1}")
			self.logger.log_age_header(age)
			self.deal_age_cards(age)
			offset = 0 # je comprends pas trop ce truc
			while len(self.decks[0]) > 1:
				self.play_turn(offset)
				offset = (offset + [1, self.player_count - 1, 1][age]) % self.player_count
			# everyone discards the last card
			for p in range(self.player_count):
				self.discard_pile.append(self.decks[p][0])
			
			# score military
			for p in range(self.player_count):
				west = self._get_west_player(p)
				east = self._get_east_player(p)
				player = self.players[p]
				player_strength, opponent_strength, score = helpers.score_military(player, west, age)
				self.logger.log_military_battle(player.get_name(), player_strength, west.get_name(), opponent_strength, score)
				self.players[p].military.append(score)
				player_strength, opponent_strength, score = helpers.score_military(player, east, age)
				self.logger.log_military_battle(player.get_name(), player_strength, east.get_name(), opponent_strength, score)
				self.players[p].military.append(score)
		for i in range(self.player_count):
			player = self.players[i]
			west = self._get_west_player(i)
			east = self._get_east_player(i)
			score = 0
			bluescore = helpers.score_blue(player)
			(_,_,_,), greenscore = helpers.score_science(player)
			score += greenscore
			redscore = 0
			for military in player.military:
				redscore += military
			moneyscore = player.money / 3
			yellowscore = helpers.score_yellow(player, west, east)
			purplescore = helpers.score_purple(player, west, east)
			player.print_tableau()
			totalscore = bluescore + greenscore + redscore + moneyscore + yellowscore + purplescore
			text = "Final score: Blue: %d, Green: %d, red: %d, yellow: %d, purple: %d, $: %d, total: %d" % (bluescore, greenscore, redscore, yellowscore, purplescore, moneyscore, totalscore)
			self.logger.log_freetext(player.get_name() + " " + text)
			print(text)
		
		logfile = open("logfile.txt", "w")
		self.logger.dump(logfile)
		logfile.close()


 
        
