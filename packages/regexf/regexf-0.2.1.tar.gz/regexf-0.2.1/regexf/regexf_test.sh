#!/bin/sh
#   author:martinmhan@yahoo.com date:  22/04/2014
#   regexf is a sh command line interface to the tango scada (and in future epics)
#   Copyright (C) <2014>  <Martin Mohan>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

#set -x
#source $(dirname $0)/regexf_unittest.sh

PASS=0
FAIL=1
export PATH=.:$PATH
#myscadat=`which scadat`
echo "`python --version` `which regexf`"

# no_match returns false=1, match returns true=0
configFile=/usr/local/bin/regexf.ini
assertequal.sh "regexf aa/bb/cc" "$configFile:re.match<aa/bb/cc> no_match"
assertfalse.sh "regexf aa/bb/cc"
assertequal.sh "regexf aa/bb/cc vac/bb/cc" "$configFile:re.match<aa/bb/cc> no_match"
assertgrep.sh "regexf vac/bb/cc -v" " match"
asserttrue.sh "regexf vac/bb/cc"
assertgrep.sh "regexf -v -f $configFile" "regexf_version"
# Even 1 no_match returns false
asserttrue.sh "regexf vac/vac1/1 vac/vac2/2" # matches return True
assertfalse.sh "regexf aa/bb/cc vac/vac1/1 vac/vac2/2" # 1 no_match return False
assertfalse.sh "regexf vac/vac1/1 aa/bb/cc vac/vac2/2" # 1 no_match return False

#configFile=regexf.ini
assertgrep.sh "regexf -f $configFile -s test1 -v" "test1"
assertgrep.sh "regexf -f $configFile -s test1 a/d/g -v" "match"
assertgrep.sh "regexf -f $configFile -s test1 d/d/g -v" " no_match"
assertgrep.sh "regexf -f $configFile -s ego_test V1:A_B/bb/cc -v" " match"
assertgrep.sh "regexf -f $configFile -s ego_test V2:A_B/bb/cc -v" " no_match"

test_file=/usr/local/bin/regexf_test.ini
assertequal.sh "regexf -f $test_file aa/bb/cc" "$test_file:re.match<aa/bb/cc> no_match"
assertfalse.sh "regexf -f $test_file aa/bb/cc"
assertequal.sh "regexf -f $test_file m/bb/cc" ""
assertgrep.sh "regexf -f $test_file -s ego -v" "A-Za-z"
assertgrep.sh "regexf -f $test_file -s ego aa/bb/cc" "$test_file:re.match<aa/bb/cc> no_match"
assertgrep.sh "regexf -f $test_file  a/bb/cc -v" " match"
assertgrep.sh "regexf -f $test_file  b/bb/cc -v" " no_match"
assertgrep.sh "regexf -f $test_file V1:A_B/bb/cc -v" " no_match"
assertgrep.sh "regexf -f $test_file -s ego V1:A_B/bb/cc -v" " match"
assertgrep.sh "regexf -f $test_file -s ego V2:A_B/bb/cc -v" " no_match"

