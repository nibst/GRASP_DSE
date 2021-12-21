from greedy import Greedy
from hillClimbing0 import HillClimbing




h1 = HillClimbing('arq_input_aes.txt','outAesHill.txt')
h1.writeSolutions()

h2 = Greedy('arq_input_gsm.txt','outGsmGreedy.txt')
h2.writeSolutions()

h3 = HillClimbing('arq_input_sha.txt','outShaHill.txt')
h3.writeSolutions()

h4 = Greedy('arq_input_span_filter.txt','outSpanGreedy.txt')
h4.writeSolutions()