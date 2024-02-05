# Intro to formal languages. Regular grammars. Finite Automata.

### Course: Formal Languages & Finite Automata
### Author: Gusev Roman

----

## Theory:
* ### Definitions:
  * **Alphabet** - is a finite, nonempty set of symbols
  * **String** - also called as "word", is a finite sequence of symbols chosen from the alphabet
  * **Length of the String** - indicates how many symbols are in mentioned string
  * **Language** - is a set of strings from an alphabet
  * **Concatenation of Strings** - is the process of putting Strings right next to each other [[1]](#bib1) 

## Objectives:

* Discover what a language is and what it needs to have in order to be considered a formal one;
* Provide the initial setup for the evolving project that you will work on during this semester. You can deal with each laboratory work as a separate task or project to demonstrate your understanding of the given themes, but you also can deal with labs as stages of making your own big solution, your own project. Do the following:
  1. Create GitHub repository to deal with storing and updating your project;
  2. Choose a programming language. Pick one that will be easiest for dealing with your tasks, you need to learn how to solve the problem itself, not everything around the problem (like setting up the project, launching it correctly and etc.);
  3. Store reports separately in a way to make verification of your work simpler (duh)
* According to my variant number (11), get the grammar definition and do the following:
  1. Implement a type/class for your grammar;
  2. Add one function that would generate 5 valid strings from the language expressed by your given grammar;
  3. Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;
  4. For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;
## Implementation description
* For the start, I had to implement and introduce the alphabet and rules that were
provided in my Variant (11). I began with defining 2 Lists for Non-Terminal Terms,
Terminal Terms, 1 Dictionary for the rules/constraints and the Start Term. After that I
instantiated a Grammar object with those Lists and Dictionary and instantiated a constant
for maximum length of words that will come in hand later.
```python
...
if __name__ == '__main__':
    print("Laboratory Work 1 - Intro to formal languages. Regular grammars. Finite Automata.")
    print("Variant: 11")
    print("Student: Gusev Roman")
    print("Group: FAF-222\n")

    # Non-Terminal Terms
    V_n = ["S", "B", "D"]
    print("Non-Terminal Terms:", V_n, "\n")

    # Terminal Terms
    V_t = ["a", "b", "c"]
    print("Terminal Terms:", V_t, "\n")

    # Rules
    P = {
        "S": ["aB", "bB"],
        "B": ["bD", "cB", "aS"],
        "D": ["b", "aD"]
    }
    print("Rules:")
    for curr_term in P:
        print(curr_term + " -> " + str(P[curr_term]))

    # Start Term
    S = "S"
    print("\nStart Term:", S)

    # Maximum Length for generated Words
    max_length = 10
...
```

* After that I designed a for loop, that will iterate exactly 5 times and will
valid words that will be stored in a List and will be used to verify if 
a word was already generated or not, and if the word is of the proper length to avoid recursion and duplicate. 
This loop will call a method from Grammar object and will generate words until all 5 are unique and have a valid length.
```python
if __name__ == '__main__':
    ...
    # Instance of Grammar Class
    grammar = Grammar.Grammar(V_n, V_t, P, S)

    # List that will store all unique Words
    generated_words = []

    # 5 iterations = 5 words
    for i in range(1, 6):
        # Generate a word
        list_of_chars = grammar.generate_string(max_length)
        if list_of_chars is None:
            exit()
        generated_word = "".join(list_of_chars)
        # Verify if the word is duplicate (is already in the list) or if word length increases maxLength
        while generated_word in generated_words or len(generated_word) > max_length or (generated_word[-1] not in P and generated_word[-1].isupper()):
            if generated_word in generated_words:
                print("\nDuplicate: " + "".join(generated_word) +
                      " (Same as Word:", str(generated_words.index(generated_word) + 1) + ")")
            elif generated_word[-1] not in P and generated_word[-1].isupper():
                print("\nNo available further derivation for: " + "".join(generated_word))
            else:
                print("\nWord is too long: " + "".join(generated_word) + " | Length: ", len(generated_word))
            print("Generating new Word...")
            generated_word = "".join(grammar.generate_string(max_length))
        # Add the generated word to the list
        generated_words.append(generated_word)
        # Output the Word
        print("\nWord:", i, ": " + "".join(generated_word) + " : Length:", len(generated_word), "\n")

    print("Generated words are: ")
    for word in generated_words:
        print("Word", generated_words.index(word) + 1, ":", word)
```

* In order to define a Grammar, I used a new class with the same name, that has
4 variables: 
  * **V_n** - List of Non-Terminal Terms;
  * **V_p** - List of Terminal Terms;
  * **P** - Contraints or Rules;
  * **S** - Starting Term;

  and defined its own Constructor, that will assign the given as arguments Lists 
  and Dictionary and Start term from Main class.
```python
...
class Grammar:
    # Constructor with some state variables as needed.
    # {V_n, V_t, P, S}
    def __init__(self, V_n, V_t, P, S):
        self.V_n = V_n
        self.V_t = V_t
        self.P = P
        self.S = S
...
```
* After this, I followed the implementation tips specified in the task Markdown file [[2]](#bib2), but
with small changes in the structure of the methods. I decided to use the mentioned 
method in the tips in the following manner:
  * First of all, I instantiated an empty String, that I used where I will build the generated string recursively
  * After that, in order to ensure a random choice of the specific rule from the rules Dictionary, I had to import 
library Random, that provides methods for random integer value
  * Now, there is the main recursive call to another method inside this class, that I will describe later in the report
I pass the previous instantiated variables - String, Start Term, maxLength of the word and Random, that will be
used inside the private method.
* To ensure stability in the code, I decided to cover all the possible edge-cases: here I check if the Start Term is a
valid Non-Terminal Term, if yes, then proceed with generation, otherwise - return empty string.
```python
import Random
...
class Grammar:
    ...
    def generate_string(self, max_length):
        # Edge-case: If Start term is not present in the Non-Terminal List, then return empty string = cannot be
        # generated string from this variables
        if self.S not in self.V_n:
            print(f"Start Symbol: {self.S} is not present in Non-Terminal Terms")
            return None

        # String used in order to append more easily and manipulate String variables
        generated_string = []
        print(f"{self.S} -> ", end="")
        # First call of the generation of the string that will go recursively
        self.__generate_next_string(generated_string, self.S, max_length)
        # Return the generated String that is formed in the end of the recursion call.
        return generated_string
    ...
```
* In the end, I will describe the main method that is responsible for the generation of the next Strings/words.
It is a method that is called recursively, takes as input values:
  * ```String List currentWord```, in which the word is built and concatenated
  * ```String term```, that is the next term that we get randomly from the Production of Rules that we have - the Map 
object P
  * ```int maxLength```, that will ensure that the word that is being generated will have a maximum length and will not
exceed it and, therefore, will ensure that there will not be infinite recursion
* First, I have to check if the current word, that is being generated, is not exceeding the maximum length
that was passed to the method. 
* If the word is longer, then I add for the sake of a pretty output, the last Non-Terminal
terms and exit recursion. Otherwise, I check if the term I got is a Non-Terminal Term, exactly if the term is contained 
in the Production of Rules that I got when Grammar object was created. 
* If the Dictionary contains such key that is equal to the term that is being analyzed, therefore the term is Non-Terminal and may be derivated further. I get the possible derivation
List for this Non-Terminal Term, then I choose one random derivation from this list,
and for each term of the derivation (every char of the derivation string), I make a recursive call to the same method I
am in currently, and go again.
* Otherwise, if the Dictionary does not contain such Term, then this Term is a Terminal Term, and is being just added to the String List currentWord
and the recursion is stopped. Also, here I check if the Term is Non-Terminal and has no derivation, then the grammar is 
not suitable for our purposes, and may lead to a word that has a Non-Terminal Term in it, and cant be derived furthemore.
```python
class Grammar:
    ...
    def __generate_next_string(self, current_word, term, max_length):
        # Edge-case: word is too long (avoid infinite recursion)
        if len(current_word) >= max_length:
            current_word.append(term[-1])  # add last non-terminal term in order to display correctly the generated word
            return  # exit recursion

        # Case: if there is a rule/produce for this specific Non-Terminal Term -> goes into recursion for the next term
        if term in self.P:
            # Get all possible derivations for current non-terminal term
            curr_derivation_list = self.P[term]

            # Get one random derivation from the Produce List
            curr_derivation = random.choice(curr_derivation_list)

            # Check if last term is Non-Terminal, then add -> at the end, else - do not add
            if curr_derivation[-1].isupper():
                print(f'{"".join(current_word)}{curr_derivation} -> ', end="")
            else:
                print(f'{"".join(current_word)}{curr_derivation}', end="")

            # For every term, iterate again recursively: ensures adding the terminal term and going for
            # the non-terminal one in another recursion
            for separate_term in curr_derivation:
                self.__generate_next_string(current_word, separate_term, max_length)
        # Case: if there is no rule/produce for this specific Non-Terminal Term -> ends recursion
        else:
            # Edge-case: if the Term is Non-Terminal and has no further derivation
            if term not in self.P and term.isupper():
                current_word.append(term)
                print(f"\nNon-Terminal Term: {term} is not present in Rules Dictionary!", end="")
            # Case: if the Term is a Terminal Term
            else:
                current_word.append(term)  # add the terminal term and exits recursion
```
* In such manner, I designed the code for the methods responsible for the generation of the words based on a set of Terminal
and Non-Terminal Terms, a Start Term and a Dictionary that maps the Terminal Term with their possible derivation into different
expressions.

## Conclusions / Screenshots / Results:
I present here one output for the Grammar Exercise of the Laboratory Work nr1.
```
Laboratory Work 1 - Intro to formal languages. Regular grammars. Finite Automata.
Variant: 11
Student: Gusev Roman
Group: FAF-222

Non-Terminal Terms: ['S', 'B', 'D'] 

Terminal Terms: ['a', 'b', 'c'] 

Rules:
S -> ['aB', 'bB']
B -> ['bD', 'cB', 'aS']
D -> ['b', 'aD']

Start Term: S
S -> aB -> acB -> accB -> acccB -> acccaS -> acccaaB -> acccaacB -> acccaaccB -> acccaacccB -> acccaaccccB -> 
Word is too long: acccaaccccB | Length:  11
Generating new Word...
S -> aB -> acB -> acaS -> acaaB -> acaabD -> acaabaD -> acaabaaD -> acaabaab
Word: 1 : acaabaab : Length: 8 

S -> bB -> bcB -> bcaS -> bcaaB -> bcaabD -> bcaabaD -> bcaabaaD -> bcaabaaaD -> bcaabaaab
Word: 2 : bcaabaaab : Length: 9 

S -> aB -> abD -> abaD -> abaaD -> abaab
Word: 3 : abaab : Length: 5 

S -> bB -> baS -> baaB -> baabD -> baabaD -> baabab
Word: 4 : baabab : Length: 6 

S -> bB -> bcB -> bcbD -> bcbb
Word: 5 : bcbb : Length: 4 

Generated words are: 
Word 1 : acaabaab
Word 2 : bcaabaaab
Word 3 : abaab
Word 4 : baabab
Word 5 : bcbb
```

## References:
<a id="bib1"></a>[1] Formal Languages and Finite Automata Guide for practical lessons - TUM - https://else.fcim.utm.md/pluginfile.php/110458/mod_resource/content/0/LFPC_Guide.pdf

<a id="bib2"></a>[2] Laboratory Work 1: Intro to formal languages. Regular grammars. Finite Automata. Task - Dumitru Crudu, Vasile Drumea, Irina Cojuhari - https://github.com/filpatterson/DSL_laboratory_works/blob/master/1_RegularGrammars/task.md