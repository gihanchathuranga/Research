%To Start the system type start.
% Name : - L.G. Chathuranga

:- use_module(library(jpl)).
start :-sleep(0.4),	
		write('-----------------------------------------------------------------'),nl,
		sleep(0.4),
		write('*****************************************************************'),nl,
		sleep(0.2),
		write("###################||| VEHICLE EXPERT SYSTEM |||#########################"),nl,
		sleep(0.4),
		write('*****************************************************************'),nl,
		sleep(0.4),
		write('-----------------------------------------------------------------'),nl,nl,nl,

		interface2.
		
    details(Customer,transport):- verify(Customer," bla bla bla (y/n) ?").
 
    details(Customer,being_active_doing_things) :- verify(Customer," care about being active doing things  (y/n) ?").
  
   	details(Customer,what_people_think_of_me) :- verify(Customer," care about what people think about you (y/n) ?").
 
	details(Customer,i_seem_rich) :- verify(Customer," want them to think you are rich(y/n) ?").
 
 	details(Customer,love_it) :- verify(Customer," like DEBT (y/n) ?").
 	
 	details(fun) :- verify(Customer," Do you find a car for fun (y/n)").

	details(being_osm):- verify(Customer," Do you want to be awsome (y/n)").

	details(going_fast) :- verify(Customer," Do you want go fast (y/n)").
	
	details(six) :- verify(Customer," How many Cylinders? six -y").
	

	

        
    find_car(Customer,honda_fit) :-
        details(Customer,transport),
        details(Customer,being_active_doing_things),
        details(Customer,4).

    find_car(Customer,mercedes_cls) :-
        details(Customer,transport),
        details(Customer,what_people_think_of_me),
        details(Customer,i_seem_rich),
        details(Customer,love_it).

    find_car(Customer,morgan):-
		details(fun),
		details(being_osm).

	find_car(Customer,porsche):-
		details(fun),
		details(going_fast),
		details(six).
       
   
        
	find_car(_,"I am sorry. I can't match your details with a car").
	
    response(Reply) :-
        read(Reply),
        write(Reply),nl.
	



ask(Customer,Question) :-
	write(Customer),write(' , '),write(Question),
	interface(' , ',Customer,Question),
	write('Loading.'),nl,
	sleep(1),
	write('Loading..'),nl,
	sleep(1),
	write('Loading...'),nl,
	sleep(1),
    nl.
	




:- dynamic yes/1,no/1.		
	
verify(P,S) :-
   (yes(S)   ->    true ;
   		(no(S)    ->    fail ;
    		ask(P,S)
    	)

   ).
	 
undo :- retract(yes(_)),fail. 
undo :- retract(no(_)),fail.
undo.


customer(Customer):- 

		find_car(Customer,CarType),
		interface3(Customer,', you probably match ',CarType,'.'),
        write(Customer),write(', you probably have '),write(CarType),write('.'),undo,end.

end :-
		nl,nl,nl,
		sleep(0.7),
		write('*****************************************************************'),nl,
		sleep(0.4),
		write("################||| THANK YOU FOR USE ME |||#####################"),nl,
		sleep(0.4),
		write('*****************************************************************'),nl.

interface(X,Y,Z) :-
	atom_concat(Y,X, FAtom),
	atom_concat(FAtom,Z,FinalAtom),
	jpl_new('javax.swing.JFrame', ['Expert System'], F),
	jpl_new('javax.swing.JLabel',['--- VEHICLE EXPERT SYSTEM ---'],LBL),
	jpl_new('javax.swing.JPanel',[],Pan),
	jpl_call(Pan,add,[LBL],_),
	jpl_call(F,add,[Pan],_),
	jpl_call(F, setLocation, [400,300], _),
	jpl_call(F, setSize, [400,300], _),
	jpl_call(F, setVisible, [@(true)], _),
	jpl_call(F, toFront, [], _),
	jpl_call('javax.swing.JOptionPane', showInputDialog, [F,FinalAtom], N),
	jpl_call(F, dispose, [], _), 
	write(N),nl,
	( (N == yes ; N == y)
      ->
       assert(yes(Z)) ;
       assert(no(Z)), fail).
	   		
interface2 :-
	jpl_new('javax.swing.JFrame', ['Expert System'], F),
	jpl_new('javax.swing.JLabel',['--- VEHICLE EXPERT SYSTEM ---'],LBL),
	jpl_new('javax.swing.JPanel',[],Pan),
	jpl_call(Pan,add,[LBL],_),
	jpl_call(F,add,[Pan],_),
	jpl_call(F, setLocation, [400,300], _),
	jpl_call(F, setSize, [400,300], _),
	jpl_call(F, setVisible, [@(true)], _),
	jpl_call(F, toFront, [], _),
	jpl_call('javax.swing.JOptionPane', showInputDialog, [F,'Hi.First of all tell me your name please'], N),
	jpl_call(F, dispose, [], _), 
	
	(	N == @(null)
		->	write('you cancelled'),interface3('you cancelled. ','Thank you ','for use ','me.'),end,fail
		;	write("Hi. First of all tell me your name please : "),write(N),nl,customer(N)
	).
	
	
interface3(P,W1,D,W2) :-
	atom_concat(P,W1, A),
	atom_concat(A,D,B),
	atom_concat(B,W2,W3),
	jpl_new('javax.swing.JFrame', ['Expert System'], F),
	jpl_new('javax.swing.JLabel',['--- VEHICLE EXPERT SYSTEM ---'],LBL),
	jpl_new('javax.swing.JPanel',[],Pan),
	jpl_call(Pan,add,[LBL],_),
	jpl_call(F,add,[Pan],_),
	jpl_call(F, setLocation, [400,300], _),
	jpl_call(F, setSize, [400,300], _),
	jpl_call(F, setVisible, [@(true)], _),
	jpl_call(F, toFront, [], _),
	jpl_call('javax.swing.JOptionPane', showMessageDialog, [F,W3], N),
	jpl_call(F, dispose, [], _), 
	
	(	N == @(void)
		->	write('')
		;	write("")
	).
	
help :- write("To start the expert system please type 'start.' and press Enter key").