#!/usr/bin/env python

from __future__ import print_function

import time
import datetime
from colorclass import Color, Windows
from terminaltables import SingleTable
import argparse
import requests
import sys
import signal

parser = argparse.ArgumentParser(description="Zcash flypool Information Gatherer")
parser.add_argument('-w', metavar='wallet_address', required=True, help='Your t Address which you are mining to')
parser.add_argument('-n', metavar='non_stop', help=' Not needed, if equals \'YES\', run the application continuously, updates tables in 2 minutes')
args = parser.parse_args()

def handler(signum, frame):
    print (Color('\n{autogreen}Bye bye!{/autogreen}'))
    exit()

signal.signal(signal.SIGINT, handler)

class FlyInfo:
    def __init__(self, wallet):
        Windows.enable(auto_colors=True, reset_atexit=True)  # For just Windows
        self.wallet_ = wallet

        self.ZEC_usd_ = 0
        self.BTC_usd_ = 0

        self.time_str_ = "Hello Buddy!"

        self.stats_table_ = []
        self.workers_table_ = []

        self.miner_  = {}
        self.worker_ = {}

        self.printDotInfo('Getting data')
        self.getValues()
        self.getStats()
        self.printStats()

        if args.n == 'YES':
            self.displayNonStop()
        else:
            exit()

    def displayNonStop(self):
        while True:
            time.sleep(120)
            self.clearLastLine()
            self.printDotInfo(str(Color(self.time_str_)))
            self.getStats()
            self.printStats()

    def clearScreen(self):
        print("\033[H\033[J")

    def clearLastLine(self):
        sys.stdout.write("\033[F")  # back to previous line
        #sys.stdout.write("\033[K")  # Clear to the end of line

    def printStats(self):
        self.clearScreen()
        print(self.stats_table_.table)
        print(self.workers_table_.table)
        self.time_str_ = time.strftime('Last update: {autoyellow}%d/%m/%Y{/autoyellow} {autocyan}%H:%M:%S {/autocyan}', datetime.datetime.now().timetuple())
        print(Color(self.time_str_))

    def printDotInfo(self, info=None):
        """ ⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏ """
        if info == None:
            if self.dot_count_ == 0:
                sys.stdout.write('\b\b\b ⠙ \b ')
                sys.stdout.flush()
                self.dot_count_ += 1
            elif self.dot_count_ == 1:
                sys.stdout.write('\b\b\b ⠹ \b ')
                sys.stdout.flush()
                self.dot_count_ += 1
            elif self.dot_count_ == 2:
                sys.stdout.write('\b\b\b ⠹ \b ')
                sys.stdout.flush()
                self.dot_count_ += 1
            elif self.dot_count_ == 3:
                sys.stdout.write('\b\b\b ⠸ \b ')
                sys.stdout.flush()
                self.dot_count_ += 1
            elif self.dot_count_ == 4:
                sys.stdout.write('\b\b\b ⠼ \b ')
                sys.stdout.flush()
                self.dot_count_ += 1
            elif self.dot_count_ == 5:
                sys.stdout.write('\b\b\b ⠴ \b ')
                sys.stdout.flush()
                self.dot_count_ += 1
            elif self.dot_count_ == 6:
                sys.stdout.write('\b\b\b ⠦ \b ')
                sys.stdout.flush()
                self.dot_count_ += 1
            elif self.dot_count_ == 7:
                sys.stdout.write('\b\b\b ⠧ \b ')
                sys.stdout.flush()
                self.dot_count_ += 1
            elif self.dot_count_ == 8:
                sys.stdout.write('\b\b\b ⠇ \b ')
                sys.stdout.flush()
                self.dot_count_ += 1
            elif self.dot_count_ == 9:
                sys.stdout.write('\b\b\b ⠏ \b ')
                sys.stdout.flush()
                self.dot_count_ += 1
            else:
                sys.stdout.write('\b\b\b ⠋ \b ')
                sys.stdout.flush()
                self.dot_count_ = 0
        else:
            sys.stdout.write(info + ' ⠋ \b ')
            sys.stdout.flush()
            self.dot_count_ = 0

    def getValues(self):
        self.ZEC_usd_ = self.getValueInOtherCurrency('ZEC', 1, 'USD', True)
        self.BTC_usd_ = self.getValueInOtherCurrency('BTC', 1, 'USD', True)

    def getValueInOtherCurrency(self, curency, amount, other_currency, use_dot=None ):
        if curency.upper() == other_currency.upper(): # No need to convert
            return amount
        url = "https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}".format(curency.upper(), other_currency.upper())
        response = requests.get(url, timeout=10)
        json_dict = response.json()
        price = json_dict[other_currency.upper()]
        value = float(price) * float(amount)
        if use_dot != None:
            self.printDotInfo()
        return value

    def getFlpJsonDict(self, command_type, wallet, method, use_dot = None):
        url="https://api-zcash.flypool.org/{}/{}/{}".format(command_type, wallet, method)
        response = requests.get(url, timeout=10)
        json_dict = {}
        try:
            json_dict = response.json()
        except ValueError:
            print()
            print()
            print(Color('{autored}Website didn\'t response with a valid json:{/autored}'))
            print(response.content)
            exit()
        if use_dot != None:
            self.printDotInfo()
        return json_dict

    def strI0(self, value): # returns integer's str or '0.0'
        try:
            return str(int(value))
        except:
            return '0'

    def strF0(self, value, perc=None): # returns float's str or '0.0'
        try:
            if perc == None:
                return str(float(value))
            else:
                return str(perc % float(value))
        except:
            return '0.0'

    def getStats(self):

        json_dict = self.getFlpJsonDict('miner', self.wallet_, 'currentStats', True)
        self.miner_ = json_dict["data"]
        json_dict = self.getFlpJsonDict('miner', self.wallet_, 'workers', True)
        self.worker_ = json_dict["data"]

        table1 = []

        unpaid = float( int(self.strI0(self.miner_["unpaid"])) ) / 100000000.0
        immatu  =float( int(self.strI0(self.miner_["unconfirmed"])) ) / 100000000.0

        row1 = [Color('{autoyellow}Immature{/autoyellow} ZEC\n{autocyan}' + str(immatu) + '{/autocyan}'),
                Color('{autoyellow}Unpaid{/autoyellow} ZEC\n{autocyan}'   + str(unpaid) + '{/autocyan}'),
                Color('{autoyellow}Current{/autoyellow}\n{autocyan}' + self.strF0(self.miner_["currentHashrate"], "%.1f" ) +'{/autocyan} H/s'),
                Color('{autoyellow}Average{/autoyellow}\n{autocyan}' + self.strF0(self.miner_["averageHashrate"], "%.1f") + '{/autocyan} H/s'),
             ]
        table1.append(row1)
        row2 = [Color('{autoyellow}ZEC {/autoyellow}${autogreen}'         + self.strF0(self.ZEC_usd_) + '{/autogreen}\n{autoyellow}BTC {/autoyellow}${autogreen}' + str(self.BTC_usd_) + '{/autogreen}'),
                Color('{autoyellow}Est. Month{/autoyellow}\n'             + self.strF0((43200 * self.miner_["coinsPerMin"]), "%.4f" ) + ' ZEC' ),
                Color('{autoyellow}Est. Month{/autoyellow}\n${autogreen}' + self.strF0((43200 * self.miner_["usdPerMin"]),  "%.4f")   +'{/autogreen}'),
                Color('{autoyellow}Est. Month{/autoyellow}\nɃ{autocyan}'  + self.strF0((43200 * self.miner_["btcPerMin"]),  "%.4f")   + '{/autocyan}'),
             ]
        table1.append(row2)

        self.stats_table_ = SingleTable(table1)
        self.stats_table_.inner_heading_row_border = False
        self.stats_table_.inner_row_border = True
        self.stats_table_.justify_columns = {0: 'center', 1: 'center', 2: 'center', 3: 'center'}

        table2 = []

        for worker in self.worker_:
            name = worker['worker']
            curr = worker['currentHashrate']
            avgr = worker['averageHashrate']
            vali = worker['validShares']
            inva = worker['invalidShares']
            row = [Color('{autoyellow}' + str(name) + '{/autoyellow}\n({autogreen}' + str(vali) + '{/autogreen},{autored}' + str(inva) + '{/autored})'),
                   Color('{autoyellow}Current{/autoyellow}\n{autocyan}'+ self.strF0(curr, "%.2f") +'{/autocyan} H/s'),
                   Color('{autoyellow}Average{/autoyellow}\n{autocyan}' + self.strF0(avgr, "%.2f") + '{/autocyan} H/s'),
                  ]
            table2.append(row)

        self.workers_table_ = SingleTable(table2)
        self.workers_table_.inner_heading_row_border = False
        self.workers_table_.inner_row_border = True
        self.workers_table_.justify_columns = {0: 'center', 1: 'center', 2: 'center', 3: 'center'}


def main():
    m = FlyInfo(args.w)

if __name__ == '__main__':
    main()
