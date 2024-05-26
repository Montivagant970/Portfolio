(define (domain minigrid)
    (:predicates
        (cell ?c)
        (agent ?a)
        (key ?k)
        (obj ?o)
        (at ?o ?c)
        (connected ?c1 ?c2)
        (hold ?a ?b)
        (free ?a)
        (locked ?l)
        (blocked ?o)
    )

    (:action move
        :parameters (?a ?c1 ?c2)
        :precondition (and (agent ?a) (cell ?c1) (cell ?c2) (at ?a ?c1) (connected ?c1 ?c2) (not (locked ?c2)) (not (blocked ?c2)))
        :effect (and (at ?a ?c2)
                     (not (at ?a ?c1)))
    )

    (:action pick
        :parameters (?a ?o ?c1 ?c2)
        :precondition (and (agent ?a) (obj ?o) (at ?a ?c1) (at ?o ?c2) (connected ?c1 ?c2) (free ?a) (blocked ?c2))
        :effect (and (hold ?a ?o) 
                     (not (at ?o ?c2))
                     (not (free ?a))
                     (not (blocked ?c2)))
    )

    (:action pick-key
        :parameters (?a ?k ?c1 ?c2)
        :precondition (and (agent ?a) (key ?k) (at ?a ?c1) (at ?k ?c2) (connected ?c1 ?c2) (free ?a) (blocked ?c2))
        :effect (and (hold ?a ?k) 
                     (not (at ?k ?c2))
                     (not (free ?a))
                     (not (blocked ?c2)))
    )

    (:action drop
        :parameters (?a ?o ?c1 ?c2)
        :precondition (and (agent ?a) (obj ?o) (at ?a ?c1) (connected ?c1 ?c2) (hold ?a ?o))
        :effect (and (at ?o ?c2)
                     (free ?a)
                     (blocked ?c2)
                     (not (hold ?a ?o)))
    )

    (:action drop-key
        :parameters (?a ?k ?c1 ?c2)
        :precondition (and (agent ?a) (key ?k) (at ?a ?c1) (connected ?c1 ?c2) (hold ?a ?k))
        :effect (and (at ?k ?c2)
                     (free ?a)
                     (blocked ?c2)
                     (not (hold ?a ?k)))
    )

    (:action unlock
        :parameters (?a ?k ?c1 ?c2)
        :precondition (and (agent ?a) (key ?k) (hold ?a ?k) (at ?a ?c1) (connected ?c1 ?c2) (locked ?c2))
        :effect (not (locked ?c2))
        )
)