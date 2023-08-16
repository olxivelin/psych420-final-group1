## Background

### What is a Memory Model?

At the most basic level computational models of memory will encode
information, store it, and then attempt to retrieve it. They are 
commonly applied to developing our understanding of how different 
kinds of learning and forgetting can occur in the brain. For this 
project we used the Multi Store Model (MSM) by Atkinson-Shiffrin 
as the inspiration for our design. We will briefly discuss the 
MSM, as well as two other memory model approaches (MINERVA 2 and 
connectionist models) that we could have used. 


### Multi Store Model (MSM)

In cases of severe epilepsy surgical removal of the epileptogenic 
focus may be indicated. Temporal lobe epilepsy represents 
approximately 2/3 of intractable seizure cases and throughout 
the 20th century it became clear that performing bilateral 
temporal lobectomies (as in the case of patient H.M.) resulted 
in profound impairments to the patient's declarative memory [(Téllez-Zenteno & Hernández-Ronquillo, 2012)](#téllez-zenteno-2012). 
In the case of H.M. following the removal of most of his 
hippocampus he could shake your hand and carry on a conversation, 
but after you left the room and his thoughts drifted from your 
encounter he'd have no memory that you were ever there. It was 
this growing recognition of the role of different brain systems 
being involved in short term vs. long term memory that inspired 
Atkinson and Shiffrin's MSM ([See Figure 1](#figure-1)) [(Shiffrin & Atkinson, 1969)](#shiffrin-atkinson-1969).  

<a id="figure-1"></a>_Figure 1: An overview of Atkinson and Shiffrin's Multi Store Model_

![Figure 1: An overview of Atkinson and Shiffrin's Multi Store Model](images/Information_Processing_Model_-_Atkinson_%26_Shiffrin.jpg)

The basis of the MSM is that the transition of information into memories 
is divided into 3 stages. Sensory Memory -> Short-Term Memory <-> 
Long Term Memory. 


#### Sensory Memory

Theoretical models of “selective attention” had their heyday in the 
1960’s as the researchers Broadbent, Treisman, and Deutsch competed 
to get their names into introductory psych textbooks… The common theme 
amongst their models is that you’re not fully aware of everything 
around you, some of the information your senses register is forgotten 
before reaching other cognitive processes [(Treisman, 1969)](#treisman-1969). That there are limits to
our processing capacity is a theme that will appear again as we’re 
discussing the short-term memory stage. 


#### Short Term Memory

Following George Miller’s rather poetic reports of how the magical 
number seven was stalking and pursuing him throughout his work the 
concept of “short-term” memory became widely established [(Miller, 1956)](#miller-1956). If you’re
provided with a list of numbers or a list of random words, there’s a 
limit to the number of items you can hold in your cognitive buffer 
before new items will displace the old. As time goes by without 
rehearsal your memories of the list will begin to decay, and the 
items will become increasingly difficult to remember correctly. 
With sufficient rehearsal, e.g., repeating a list over and over, it is
possible to move memories into a more stable long-term storage from 
which they can later be retrieved [(Cowan, 2008)](#cowan-2008).

#### Long Term Memory

The early work of Ebbinghaus demonstrates that while memories stored 
in the long term stage are more enduring than those held in the 
short-term stage the passage of time will make retrieval increasingly 
difficult [(Murre & Dros, 2015)](#murre-dros-2015). 
The retention of information can also be disrupted by 
the presence of similar or competing information, this can occur 
proactively when previously acquired knowledge needs to be unlearned 
e.g., you have to change your password because the university got 
hacked [(Bass & Oswald, 2014)](#bass-oswald-2014). Or it can occur retroactively when new information makes 
it difficult to remember existing details e.g., after using Emacs 
exclusively for 2 years you find you’ve forgotten the keyboard 
shortcuts in Microsoft Word [(Sosic-Vasic et al., 2018)](#sosic-vasic-et-al-2018).

While the process of retrieval in the MSM model is typically 
represented with memories being encoded as discrete units. 
Modern theoretical understandings of “engrams” (i.e., units of 
cognitive information) suggest that memories are distributed 
throughout the brain with structures like the hippocampus acting 
as an indexing agent [(Teyler & Rudy, 2007)](#teyler-rudy-2007). In practice this means that different 
aspects of memory like the logical semantic definition of a word 
(e.g., murder = unjustifiable homicide) and the affective dimensions
of that word (e.g., murder = bad) can be stored independently. 

Recall the temporal lesion patients that originally inspired the MSM.
With further investigation it became clear that their anterograde 
amnesia only affected certain memory domains. Patient H.M. for 
instance became increasingly proficient at drawing stars in a mirror
(a procedural memory task) [(Squire, 2009)](#squire-2009).
In another example Édouard Claparède 
was an early Swiss neurologist who is notorious for shaking the hand
of one of his patient’s while holding a concealed pin. 
Leaving and returning shortly thereafter he reports the patient had 
forgotten the episodic details of the handshake but was unwilling to 
shake Claparède’s hand a second time despite not having a clearly
articulable reason for their hesitancy (an example of behavioral 
conditioning) [(Feinstein et al., 2010)](#feinstein-et-al-2010).
The significance of these findings is that they 
demonstrate that there are different forms of long term memory 
that aren’t well represented as a single stage in the MSM [(Fox et al., 2017)](#fox-et-al-2017).

### Emotion and Memory

The emotional dimensions of valence and arousal have been 
demonstrated to engage distinct cognitive and neural processes 
contributing to enhanced memory [(Kensinger & Corkin, 2004)](#kensinger-corkin-2004). Brown and Kulik’s work on 
“flashbulb memories” (i.e., memories of highly emotional episodic 
events like 9/11 or the Challenger disaster) reinforced earlier 
notions that emotional memories were indelible. Further research 
has demonstrated that the vivid detail often associated with 
memories for emotional events doesn’t mean that those memories 
are necessarily accurate. Even the memories for the emotions 
themselves can be subject to manipulation, in one example students 
asked to recall their emotional state before and after receiving an 
exam grade will tend to overestimate their feelings of anxiety after 
receiving a poor mark [(Levine & Pizarro, 2004)](#levine-pizarro-2004). 

### Logic vs. Emotion

Prior memory models have investigated how semantic relatedness along 
logical dimensions influences memory and learning [(McClelland et al., 1995)](#mcclelland-et-al-1995).
We thought it would be interesting to instead explore how random 
drift along affective dimensions could impact memory over time. 
There is evidence that some material due to its affective dimensions 
is more likely to be stored and recalled when one is in a particular 
mood [(Ucros, 1989)](#ucros-1989). We wanted to explore the idea that 
when presented with a 
stimulus if we encode the affective dimensions of that stimulus, how 
effective a memory trace based on those emotional characteristics 
might be (in practice this turned out to not actually be very 
effective.. but we’ll discuss that more later on). The PAD (pleasure,
arousal, dominance) model developed by Russell and Mehrabian tries 
to characterize human emotional experiences along three dimensions 
(see [Figure 2](#figure-2)) [(Russell & Mehrabian, 1977)](#russell-mehrabian-1977).
To encode stimuli with these dimensions we used 
Warriner’s database of lexical norms [(Warriner et al., 2013)](#warriner-et-al-2013).

<a id="figure-2"></a>_Figure 2: PAD (pleasure, arousal, dominance) model_

![PAD (pleasure, arousal, dominance) model](images/avd.png)

### Connectionist Models

While we drew upon the MSM as the inspiration for our memory model 
primarily due to its simplicity, there are other approaches that 
we could have taken. Connectionist models have several advantages:

 - They’re able to represent different features of memory in a  
   hierarchical structure in a way that explains how we’re able to 
   integrate common features of semantic knowledge (e.g., a rose is 
   a living thing, a flower, and it’s pretty). [Figure 3](#figure-3) provides a  
   good example of how information can be 
   hierarchically represented as a tree.
 - They’re able to represent that different types of long-term memory 
   can be distributed between systems like the hippocampus and the  
   neocortex such that the learning rate of higher order integrations
   of knowledge and understanding vs. the simple memorization of 
   lists can be represented by distinct systems with their own 
   learning rate. [Figure 4](#figure-4) demonstrates how the same information from
   [Figure 3](#figure-3) can be represented as a neural network.  

A limitation of connectionist models is that they’re prone to 
catastrophic forgetting when they attempt to emulate learning and 
memory on integrated learning tasks (e.g., tasks that require 
memorizing two interleaved lists of items) [(McClelland et al., 1995)](#mcclelland-et-al-1995).[15]

<a id="figure-3"></a>_Figure 3: A tree-like hierarchical representation of semantic knowledge that forms the basis of connectionist models._ 

![A tree-like hierarchical representation of semantic knowledge](images/semantic_tree.png)

<a id="figure-4"></a>_Figure 4: A neural network representation of semantic knowledge_

![A neural network representation of semantic knowledge(images/neural_network.png) 


### Minerva 2
Developed by James Hintzman in the 1980’s, Minerva 2 represents 
memories as being distributed across a network of interconnected 
nodes. These nodes can include features from multiple systems, and 
collectively each set of features is called a “memory trace”. 
Whenever the system encounters a new stimulus a “probe” representing 
the features of the stimulus will run through the network activating 
memory traces. The sum of these activations can be thought of as an 
“echo”, and if the collective echo reaches a certain threshold the 
system will “recognize” the stimuli, if the echo does not reach the 
threshold, then it will not recognize the stimulus ([Figure 5](#figure-5)) [(Hintzman, 1984)](#hintzman-1984).

<a id="figure-5"></a>_Figure 5: A representation of multiple memory traces in a Minerva model, in which a stimulus is being compared with existing memories on variety of perceptual dimensions._

![A representation of multiple memory traces in a Minerva model](images/Minerva.png)

