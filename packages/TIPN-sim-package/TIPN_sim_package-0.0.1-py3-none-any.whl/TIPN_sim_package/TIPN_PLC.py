class Place:
    def __init__(self, name, p_type, holding, marking):
        """
        Place vertex in the petri net.
        :name: Identity
        :p_type: Manual, observable or unobservable
        :holding: Corresponding output and its level
        :marking: Tokens at the place
        """
        self.name = name
        self.p_type = p_type
        self.holding = holding
        self.marking = marking

    def publish(self):
        """
        Publish output level value (when transition is fired
        """
        if self.p_type == 'o':
            print(self.name, ' observable place', self.holding, ':', self.marking)
            if self.marking == 1:
                Sim.update_val(self.holding, True)
            elif self.marking == 0:
                Sim.update_val(self.holding, False)
            else:
                print('output place marking >1 !')

        elif self.p_type == 'u':
            print(self.name, ' unobservable place', self.holding, ':', self.marking)
        elif self.p_type == 'wp':
            print(self.name, ' waiting place', self.holding, ':', self.marking)
        elif self.p_type == 'manual':
            print(self.name, 'manual', self.holding, ':', self.marking)
            Sim.update_val(self.holding, self.marking)
        else:
            print(self.name, ' has a wrong type !')


class ArcBase:
    def __init__(self, place, weight=1):
        """
        Arc in the petri net.
        :place: The one place acting as source/target of the arc as arc in the net
        :amount: The amount of token removed/added from/to the place.
        """
        self.place = place
        self.weight = weight


class Out(ArcBase):
    def trigger(self):
        """
        Remove token.
        """
        self.place.marking -= self.weight
        self.place.publish()

    def non_blocking(self):
        """
        Validate action of outgoing arc is possible.
        """
        return self.place.marking >= self.weight


class In(ArcBase):
    def trigger(self):
        """
        Add tokens.
        """
        self.place.marking += self.weight
        self.place.publish()


class Transition:
    def __init__(self, name, out_arcs, in_arcs, condition, delay):
        """
        Transition vertex in the petri net.
        :name: name to identify
        :out_arcs: Collection of ingoing arcs, to the transition vertex.
        :in_arcs: Collection of outgoing arcs, to the transition vertex.
        :condition: triggering condition
        :delay: delay (from the previous transition)
        """
        self.name = name
        self.out_arcs = set(out_arcs)
        self.arcs = self.out_arcs.union(in_arcs)
        self.condition = condition
        self.delay = delay

    def fire(self):
        """
        Fire!
        """
        not_blocked = all(arc.non_blocking() for arc in self.out_arcs)
        # Note: This would have to be checked differently for variants of
        # petri  nets that take more than once from a place, per transition.
        if not_blocked:
            for arc in self.arcs:
                arc.trigger()
        return not_blocked  # return if fired, just for the sake of debugging


class PetriNet:
    def __init__(self):
        """
        The petri net runner.
        """
        self.places = []
        self.transitions = []

    def build_places(self, places, gamma, zeta, m_0):
        """
        Initialize places and also adds their relation to the sensors
        """
        self.places = [Place(places[p_i], gamma[p_i], zeta[p_i], m_0[p_i]) for p_i in range(len(places))]

    def build_transitions(self, transitions, places_pre, places_post, beta, beta_t):
        """
        Initialize transitions
        """
        for t_i in range(len(transitions)):
            pre_list = []
            post_list = []
            for j in range(len(self.places)):
                if places_pre[j][t_i] != 0:
                    pre_list_j = Out(self.places[j], places_pre[j][t_i])
                    pre_list.append(pre_list_j)
                if places_post[j][t_i] != 0:
                    post_list_j = In(self.places[j], places_post[j][t_i])
                    post_list.append(post_list_j)
            temp_var = Transition(transitions[t_i], pre_list, post_list, beta[t_i], beta_t[t_i])
            self.transitions.append(temp_var)


class Obj:

    def __init__(self, obj_type, t_start, petri_net):
        """
        Instantiate an object
        :obj_type: 'metal' or 'plastic
        :t_start: starting time of the journey
        :petri_net: environment
        """

        self.obj_type = obj_type
        self.t_start = t_start
        self.sequence = self.gen_seq(petri_net)
        self.sequence_copy = self.sequence[:]

    def gen_seq(self, petri_net):
        """
        Generates the triggering sequence
        : petri_net: environment that object travels
        :return: triggering sequence
        """
        seq_temp = []
        tr = [tr.name for tr in petri_net.transitions]
        tr_delay = [tr.delay for tr in petri_net.transitions]
        # TODO remove the transition for plastic
        if self.obj_type == 'plastic':
            pass
        else:
            pass
        len_tr = len(tr)
        tr_copy = tr[:]
        beta_copy = tr_delay[:]
        helper = []
        while len(seq_temp) < len_tr:
            for i in range(len(tr)):
                temp = {}
                name = tr[i]
                condition = tr_delay[i]
                con = [*condition][0]
                delay = condition[con]
                if con == 'start':
                    temp['name'] = name
                    temp['delay'] = delay
                    helper.append(name)
                    seq_temp.append(temp)
                    tr_copy.remove(name)
                    beta_copy.remove(condition)

                elif con in helper:
                    idx = helper.index(con)
                    t_pre = seq_temp[idx]['delay']
                    temp['name'] = name
                    temp['delay'] = delay + t_pre
                    helper.append(name)
                    seq_temp.append(temp)
                    tr_copy.remove(name)
                    beta_copy.remove(condition)

                else:
                    pass

            tr = tr_copy[:]
            tr_delay = beta_copy[:]
        seq = sorted(seq_temp, key=lambda d: d['delay'])
        return seq


class Sim:
    plc = None
    current_obj = []
    start = 0
    end = 0
    status = [{'output': 'O1', 'value': False}, {'output': 'O2', 'value': False}, {'output': 'O3', 'value': True}]

    @classmethod
    def on_machine(cls):
        plc_p = ['P0', 'P1', 'P2', 'P3', 'P4']
        plc_zeta = ['manual', 'o', 'o', 'o', 'manual']
        plc_gamma = ['start', 'O1', 'O2', 'O3', 'end']  # start must be the 0th and end must be the last
        plc_tr = ['plc_t1', 'plc_t2', 'plc_t3']
        plc_beta = ['cond1', 'cond2', 'cond3']
        plc_beta_t = [{'start': 0}, {'plc_t1': 2}, {'plc_t2': 2.5}]
        plc_pre = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 0], [0, 0, 0]]
        plc_pos = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 1, 0], [0, 0, 1]]
        plc_m = [0, 0, 0, 1, 0]

        cls.plc = PetriNet()
        cls.plc.build_places(plc_p, plc_zeta, plc_gamma, plc_m)
        cls.plc.build_transitions(plc_tr, plc_pre, plc_pos, plc_beta, plc_beta_t)

    @classmethod
    def insert_obj(cls, time_start):
        cls.current_obj.append(Obj('metal', time_start, cls.plc))
        cls.plc.places[0].marking += 1
        cls.plc.places[0].publish()

    @classmethod
    def remove_obj(cls):
        cls.current_obj.remove(cls.current_obj[0])

    @classmethod
    def update_val(cls, p_name, value):
        if type(value) == bool:
            for dict_i in cls.status:
                if p_name == dict_i['output']:
                    dict_i['value'] = value
        elif type(value) == int:
            if p_name == 'start':
                cls.start = value
            elif p_name == 'end':
                cls.end = value
            else:
                print(p_name, '-', value, ': wrong place name !')

        else:
            print(p_name, '-', value, ': wrong value !')

    @classmethod
    def run_sim_step(cls, place_obj, time_n):
        if place_obj:
            cls.insert_obj(time_n)
        for objs in cls.current_obj:
            obj_seq = objs.sequence_copy
            time_0 = objs.t_start
            t_delta = time_n - time_0
            obj_seq_copy = obj_seq[:]
            for i in range(len(obj_seq)):
                if obj_seq[i]['delay'] <= t_delta:
                    print('Myself:',objs,'tr available!', obj_seq[i]['name'], time_n)
                    for tr in cls.plc.transitions:
                        if obj_seq[i]['name'] == tr.name:
                            if tr.fire():
                                print("{} fired!".format(tr.name))
                            else:
                                print("{} ...fizzled.".format(tr.name))
                    obj_seq_copy.remove(obj_seq[i])
            objs.sequence_copy = obj_seq_copy[:]
        return cls.start,cls.end,cls.status


