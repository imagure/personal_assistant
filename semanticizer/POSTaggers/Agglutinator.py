"""
@author: ricardo imagure
"""
import json
from semanticizer import entity_class as ec

with open("configs/semanticizer_literals.json") as f:
    data = json.load(f)

n_tags = data["noun_tags"]
prop_tags = data["prop_tags"]
adj_tags = data["adj_tags"]
num_tags = data["num_tags"]
v_tags = data["verb_tags"]
aglut_preps = data["aglut_preps"]
aglut_conjs = data["aglut_conjs"]


class Agglutinator:

    def __init__(self, input_text, entities_pile):
        self.input_text = input_text
        self.entities_pile = entities_pile
        self.agglutinated_entities_list = []

    def agglutinate(self):
        while len(self.entities_pile) != 0:

            # Se tem apenas 1 dá append na lista final
            if len(self.entities_pile) == 1:
                self.agglutinated_entities_list.append(self.entities_pile[0])
                self.entities_pile.remove(self.entities_pile[0])

            # Se tem mais de um, tenta aglutinar
            else:
                current_entity = self.entities_pile[0]
                next_entity = self.entities_pile[1]

                # Aglutinator 1: Aglutina entidades consecutivas
                if next_entity.start - current_entity.end == 1 \
                        and (next_entity.pos in adj_tags and current_entity.pos in n_tags         # junta subst + adj
                            or next_entity.pos in n_tags and current_entity.pos in adj_tags       # junta adj + subst
                            or next_entity.pos in n_tags and current_entity.pos in n_tags         # junta subst + subst
                            or next_entity.pos in n_tags and current_entity.pos in num_tags):     # junta num + subst
                    self.agg_consecutive_words(current_entity, next_entity, 'NP', 'agg')
                if next_entity.start - current_entity.end == 1 \
                        and (next_entity.pos in prop_tags and current_entity.pos in n_tags        # junta subst + propn
                            or next_entity.pos in n_tags and current_entity.pos in prop_tags
                            or next_entity.pos in prop_tags and current_entity.pos in prop_tags):    # junta propn + subst
                    self.agg_consecutive_words(current_entity, next_entity, 'NP', 'prop')

                # Aglutinator 2: Aglutina se houver preposições "de","da" ou "do" no meio
                elif next_entity.start - current_entity.end == 4 \
                        and self.input_text[current_entity.end + 1: next_entity.start - 1] in aglut_preps:
                    self.agg_middle_words(current_entity, next_entity, 'NP', 'agg')

                # Aglutinador 3: Aglutina expressões do tipo "semana que vem"
                elif next_entity.start - current_entity.end == 5 \
                        and self.input_text[current_entity.end + 1: next_entity.start - 1] in aglut_conjs:
                    self.agg_middle_words(current_entity, next_entity, 'NPVP', 'agg')

                # Se nenhuma condição for verdadeira, apenas dá append no current_chunk
                else:
                    # print("This is the chunk added: " + current_chunk.text)
                    del self.entities_pile[0]
                    self.agglutinated_entities_list.append(current_entity)

        return self.agglutinated_entities_list

    def agg_consecutive_words(self, current_entity, next_entity, tag, pos):
        del self.entities_pile[1]
        del self.entities_pile[0]
        joined_chunk_text = current_entity.text + " " + next_entity.text
        joined_chunk = ec.Entity(text=joined_chunk_text, start=current_entity.start,
                                 end=next_entity.end, tag=tag, pos=pos)
        self.entities_pile.insert(0, joined_chunk)

    def agg_middle_words(self, current_entity, next_entity, tag, pos):
        aglut = self.input_text[current_entity.end + 1: next_entity.start - 1]
        del self.entities_pile[1]
        del self.entities_pile[0]
        joined_chunk_text = current_entity.text + " " + aglut + " " + next_entity.text
        joined_chunk = ec.Entity(text=joined_chunk_text, start=current_entity.start,
                                 end=next_entity.end, tag=tag, pos=pos)
        self.entities_pile.insert(0, joined_chunk)
