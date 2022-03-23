Steven Necola - NLP

# Instructions:

<p> Required files: (in the same directory) </p>
<ol>
<li>main.py</li>
<li>train-Spring2022.txt</li>
<li>test.txt</li>
</ol>
<p>Generated by main.py (also included in tar)</p>
<ol>
<li>testPreprocessed.txt</li>
<li>testUnk.txt</li>
<li>trainPreprocessed.txt</li>
<li>trainUnk.txt</li>
</ol>

<p>You should be able to run the main.py file with the python command or any other means of running python file.</p>

## If you encounter an issue with compiling

<p>I've run into an issue with python versioning where the line:</p>
<code>with open ('train-Spring2022.txt','r', encoding='utf8') as f:</code>
<p>will fail to compile due to the encoding parameter not being required, however, for my machine it was required. I'm using Python version  3.8.4.
I hope not but if for any reason this causes an issue, please use the find and replace feature to replace:</p>
<code>, encoding='utf8'</code>
with a space to remove it.
