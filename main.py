import random

NB_BARS = 1
NB_OF_BEATS_PER_BAR = 4
NUMBER_OF_QUARTER_NOTES_PER_BEAT = 4
SUBDIVISIONS = 4  # doubles

NB_SUBDIVISIONS = NB_OF_BEATS_PER_BAR * SUBDIVISIONS


QUARTER_NOTE = "QN"
QUARTER_NOTE_DOT = "QND"
EIGHTH_NOTE = "EN"
EIGHTH_NOTE_DOT = "END"
SIXTEENTH_NOTE = "SN"
QUARTER_REST = "QR"
QUARTER_REST_DOT = "QRD"
EIGHTH_REST = "ER"
EIGHTH_REST_DOT = "ERD"
SIXTEENTH_REST = "SR"
BEAT_SEPARATOR = "/"
BAR_SEPARATOR = "|"
SPACE = " "

# dictionary associating a note duration to a number of sixteenth notes
note_duration_dict = {
    QUARTER_NOTE: 4,
    EIGHTH_NOTE_DOT: 3,
    EIGHTH_NOTE: 2,
    SIXTEENTH_NOTE: 1,
}
rest_duration_dict = {
    QUARTER_REST: 4,
    EIGHTH_REST_DOT: 3,
    EIGHTH_REST: 2,
    SIXTEENTH_REST: 1,
}


def get_highest_note_duration_from_available_space(available_space):
    for key in note_duration_dict:
        if note_duration_dict[key] <= available_space:
            return key
    return None


def get_highest_rest_duration_from_available_space(available_space):
    for key in rest_duration_dict:
        if rest_duration_dict[key] <= available_space:
            return key
    return None


def get_is_beat_completed(sixteenth_note_counter_in_beat):
    return sixteenth_note_counter_in_beat == NUMBER_OF_QUARTER_NOTES_PER_BEAT


# returns the sequence as a list of lists [number, boolean] where the boolean indicates if the beat has been written or not
def generate_formatted_sequence_for_treatment(sequence):
    formatted_sequence = []
    for note in sequence:
        formatted_sequence.append([note, False])
    return formatted_sequence


def generate_sequence(SUBDIVISIONS, NB_BARS=1, NB_OF_BEATS_PER_BAR=4):
    marker = 0
    note_duration = 0
    note_sequence = []
    while marker < NB_SUBDIVISIONS:
        note_duration = int(random.gauss(int(NB_SUBDIVISIONS / 4), 1))
        # note_duration = random.randint(1,NB_SUBDIVISIONS)
        marker += note_duration
        if marker < NB_SUBDIVISIONS and note_duration > 0:
            note_sequence.append(note_duration)

    note_sequence.append(NB_SUBDIVISIONS - sum(note_sequence))

    return note_sequence


def generate_bar_from_number_sequence(sequence):
    bar = ""
    treatment_sequence = generate_formatted_sequence_for_treatment(sequence)
    treating_note_index = 0
    for _ in range(NB_OF_BEATS_PER_BAR):
        available_space_in_beat = NUMBER_OF_QUARTER_NOTES_PER_BEAT
        while available_space_in_beat > 0:
            if treatment_sequence[treating_note_index][0] <= available_space_in_beat:
                if treatment_sequence[treating_note_index][1] == False:
                    bar += (
                        get_highest_note_duration_from_available_space(
                            treatment_sequence[treating_note_index][0]
                        )
                        + SPACE
                    )
                    treatment_sequence[treating_note_index][1] = True
                else:
                    bar += (
                        get_highest_rest_duration_from_available_space(
                            treatment_sequence[treating_note_index][0]
                        )
                        + SPACE
                    )
                available_space_in_beat -= treatment_sequence[treating_note_index][0]
                treatment_sequence[treating_note_index][0] = 0
                treating_note_index += 1
            else:
                if treatment_sequence[treating_note_index][1] == False:
                    bar += (
                        get_highest_note_duration_from_available_space(
                            available_space_in_beat
                        )
                        + SPACE
                    )
                    treatment_sequence[treating_note_index][1] = True
                else:
                    bar += (
                        get_highest_rest_duration_from_available_space(
                            available_space_in_beat
                        )
                        + SPACE
                    )
                treatment_sequence[treating_note_index][0] -= available_space_in_beat
                available_space_in_beat = 0
        bar += BEAT_SEPARATOR + SPACE
    return bar


for _ in range(5):
    sequence = generate_sequence(4)
    text_bar = generate_bar_from_number_sequence(sequence)
    print(sequence)
    print(text_bar)
    print("\n")
