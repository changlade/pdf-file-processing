write a python code that reads the pdf file attached and store the content and page numbers in a pickle file. You can use Spark.

build a simple web front end with a single page to explore my pdf document. It should run as a local app on port 8000
The page is divided in 2 parts. On the right side of the screen, it shows the pdf file "jugement". This file is scrollable and it should be easy to navigate its pages.
The left side of the screen is a panel where blocks of text are displayed. Those blocks are all the block of text from the pdf that contains references to CAR, formatted this way: CAR-OTP-xxxx-xxxx, les CAR-D29-xxxx-xxxx et les CAR-V45-xxxx-xxxx. Add a filter to this left panel to filter on any CAR reference that you will find in the document. If there is multiple CAR references for 1 CAR, display multiple blocks of text, that are scrollable. Clicking on one of these blocks should update the pdf view to point on this block, and highlight it. Use the json file available to extract those CAR references and put it in another JSON


-------
I want to build a RAG solution using the data from this pdf file. 
You need to find the right logic to chunk the data based on these indications: 
- Pages 1 to 6 should be ignored
- After page 6, all pages follow the same structure: a first part of main text, a second part with footnotes
- It is a legal document. I want to you to chunk intelligently to avoid breaking meaningful part of text

Explore the data and propose a chunking logic
------

Main part are following this pattern with numbered statements: 

128. As is clear from its plain meaning, reasonable doubts must be grounded in reasons.
Reasonable doubts cannot consist of imaginary or frivolous doubt – they must have a rational
link to the evidence, lack of evidence or inconsistencies in the evidence.41

129.The possibility that unavailable evidence may include exculpatory information is too
hypothetical, without more, to qualify as a reasonable doubt. Accepting such a proposition
is akin to requiring proof beyond all doubt, while what is required is instead proof beyond
reasonable doubt.42

While footnotes are as follow:

39 Appeals Chamber, The Prosecutor v. Thomas Lubanga Dyilo, Judgment on the appeal of Mr Thomas Lubanga
Dyilo against his conviction, 1 December 2014, ICC-01/04-01/06-3121-Conf (A5) (public redacted version notified
the same day, ICC-01/04-01/06-3121-Red) (the ‘Lubanga Appeals Judgment’), para. 22; Appeals Chamber, The
Prosecutor v. Mathieu Ngudjolo Chui, Judgment on the Prosecutor’s appeal against the decision of Trial Chamber II
entitled “Judgment pursuant to article 74 of the Statute”, 7 April 2015, ICC-01/04-02/12-271-Corr (the ‘Ngudjolo
Appeals Judgment’), paras 123-125; Appeals Chamber, The Prosecutor v. Jean-Pierre Bemba Gombo et al., Judgment
on the appeals of Mr Jean-Pierre Bemba Gombo, Mr Aimé Kilolo Musamba, Mr Jean-Jacques Mangenda Kabongo,
Mr Fidèle Babala Wandu and Mr Narcisse Arido against the decision of Trial Chamber VII entitled “Judgment
pursuant to Article 74 of the Statute”, 8 March 2018, ICC-01/05-01/13-2275-Conf (A A2 A3 A4 A5) (public redacted
version notified the same day, ICC-01/05-01/13-2275-Red) (the ‘Bemba et al. Appeals Judgment’), paras 96, 868;
Appeals Chamber, The Prosecutor v. Bosco Ntaganda, Judgment on the appeals of Mr Bosco Ntaganda and the
Prosecutor against the decision of Trial Chamber VI of 8 July 2019 entitled ‘Judgment’, 30 March 2021, ICC-01/04-
02/06-2666-Conf (public redacted version notified the same day, ICC-01/04-02/06-2666-Red) (the ‘Ntaganda
Appeals Judgment’), para. 37; Appeals Chamber, The Prosecutor v. Dominic Ongwen, Judgment on the appeal of Mr
Ongwen against the decision of Trial Chamber IX of 4 February 2021 entitled “Trial Judgment”, 15 December 2022,
ICC-02/04-01/15-2022-Conf (public redacted version notified the same day, ICC-02/04-01/15-2022-Red) (the
‘Ongwen Appeals Judgment’), para. 321.
40 Lubanga Appeals Judgment, ICC-01/04-01/06-3121-Red, para. 22; Trial Chamber VI, The Prosecutor v. Bosco
Ntaganda, Judgment, 8 July 2019, ICC-01/04-02/06-2359 (with public Annexes A-C) (the ‘Ntaganda Trial
Judgment’), para. 45; Trial Chamber X, The Prosecutor v. Al Hassan Ag Abdoul Aziz Ag Mohamed Ag Mahmoud,
Trial Judgment (with three public annexes), 26 June 2024, ICC-01/12-01/18-2594-Conf (public redacted version
notified the same day, ICC-01/12-01/18-2594-Red) (the ‘Al Hassan Trial Judgment’), para. 19.
41 Ngudjolo Appeals Judgment, ICC-01/04-02/12-271-Corr, para. 109, referring to ICTR, Appeals Chamber, Georges
Anderson Nderubumwe Rutaganda v. The Prosecutor, Judgement, 26 May 2003, ICTR-96-3-A, para. 488; Al Hassan
Trial Judgment, ICC-01/12-01/18-2594-Red, para. 20.
42 Trial Chamber IX, The Prosecutor v. Dominic Ongwen, Trial Judgment, 4 February 2021, ICC-02/04-01/15-1762-
Conf (public redacted version notified the same day, ICC-02/04-01/15-1762-Red) (the ‘Ongwen Trial Judgment’),
ICC-02/04-01/15-1762-Red, para. 229; Al Hassan Trial Judgment, ICC-01/12-01/18-2594-Red, para. 20.

In this example, you can also see that each footnotes have markers (in this sample, we have footnotes 39 to 42) and are referenced in the text (for example this phrase points to 42: Accepting such a proposition
is akin to requiring proof beyond all doubt, while what is required is instead proof beyond
reasonable doubt.42)

While chunking, do not mix footnotes and statements. Do not break statements. Use a chunk size that is optimized for RAG

Each page begin by something like this: ICC-01/14-01/18-2784-Red 24-07-2025 41/1616 T 
In this sample, 41/1616 means page 41 over 1616

Each page finishes by something like this: 
No. ICC-01/14-01/18 42/1616 24 July 2025
again here, 42/1616 means page 42 over 1616

Along with the chunks, retrieve associated metadata (page number, statement numbers, footnote numbers)
