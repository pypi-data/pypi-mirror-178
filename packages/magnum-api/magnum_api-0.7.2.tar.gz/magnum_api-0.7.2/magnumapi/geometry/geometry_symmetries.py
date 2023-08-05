from copy import deepcopy


typexy_and_symm_to_fun = {(0, 0): lambda layer_blocks: layer_blocks,
                          (0, 2): lambda layer_blocks: layer_blocks,
                          (0, 4): lambda layer_blocks: layer_blocks,
                          (0, 6): lambda layer_blocks: layer_blocks,
                          (0, 8): lambda layer_blocks: layer_blocks,
                          (0, 10): lambda layer_blocks: layer_blocks,
                          (0, 12): lambda layer_blocks: layer_blocks,
                          (0, 31): lambda layer_blocks: layer_blocks,
                          (0, 33): lambda layer_blocks: layer_blocks,
                          (0, 41): lambda layer_blocks: layer_blocks,
                          (1, 0): lambda layer_blocks: layer_blocks,
                          (1, 2): lambda layer_blocks: handle_all_symmetry_2_4_6_8_10_12(layer_blocks, symm=2),
                          (1, 4): lambda layer_blocks: handle_all_symmetry_2_4_6_8_10_12(layer_blocks, symm=4),
                          (1, 6): lambda layer_blocks: handle_all_symmetry_2_4_6_8_10_12(layer_blocks, symm=6),
                          (1, 8): lambda layer_blocks: handle_all_symmetry_2_4_6_8_10_12(layer_blocks, symm=8),
                          (1, 10): lambda layer_blocks: handle_all_symmetry_2_4_6_8_10_12(layer_blocks, symm=10),
                          (1, 12): lambda layer_blocks: handle_all_symmetry_2_4_6_8_10_12(layer_blocks, symm=12),
                          (1, 31): lambda layer_blocks: handle_symmetry_31(layer_blocks),
                          (1, 33): lambda layer_blocks: handle_symmetry_33(layer_blocks),
                          (1, 41): lambda layer_blocks: handle_symmetry_41(layer_blocks),
                          (2, 0): lambda layer_blocks: layer_blocks,
                          (2, 2): lambda layer_blocks: handle_one_coil_symmetry_2_4_6_8_10_12(layer_blocks, symm=2),
                          (2, 4): lambda layer_blocks: handle_one_coil_symmetry_2_4_6_8_10_12(layer_blocks, symm=4),
                          (2, 6): lambda layer_blocks: handle_one_coil_symmetry_2_4_6_8_10_12(layer_blocks, symm=6),
                          (2, 8): lambda layer_blocks: handle_one_coil_symmetry_2_4_6_8_10_12(layer_blocks, symm=8),
                          (2, 10): lambda layer_blocks: handle_one_coil_symmetry_2_4_6_8_10_12(layer_blocks, symm=10),
                          (2, 12): lambda layer_blocks: handle_one_coil_symmetry_2_4_6_8_10_12(layer_blocks, symm=12),
                          (2, 31): lambda layer_blocks: handle_symmetry_31(layer_blocks),
                          (2, 33): lambda layer_blocks: handle_symmetry_33(layer_blocks),
                          (2, 41): lambda layer_blocks: handle_symmetry_41(layer_blocks),
                          (3, 0): lambda layer_blocks: layer_blocks,
                          (3, 2): lambda layer_blocks: handle_connection_side_2_4_6_8_10_12(layer_blocks, symm=2),
                          (3, 4): lambda layer_blocks: handle_connection_side_2_4_6_8_10_12(layer_blocks, symm=4),
                          (3, 6): lambda layer_blocks: handle_connection_side_2_4_6_8_10_12(layer_blocks, symm=6),
                          (3, 8): lambda layer_blocks: handle_connection_side_2_4_6_8_10_12(layer_blocks, symm=8),
                          (3, 10): lambda layer_blocks: handle_connection_side_2_4_6_8_10_12(layer_blocks, symm=10),
                          (3, 12): lambda layer_blocks: handle_connection_side_2_4_6_8_10_12(layer_blocks, symm=12),
                          (3, 31): lambda layer_blocks: handle_symmetry_31(layer_blocks),
                          (3, 33): lambda layer_blocks: handle_symmetry_33(layer_blocks),
                          (3, 41): lambda layer_blocks: handle_symmetry_41(layer_blocks),
                          }


def build_symmetric_block_areas(geometry) -> list:
    symmetric_blocks = []
    n_blocks = geometry._calc_no_defined_blocks()
    for layer_def in geometry.layer_defs:
        layer_blocks = [next(filter(lambda x: x.block_def.no == block_index, geometry._blocks))
                        for block_index in layer_def.blocks[:n_blocks]]

        typexy_symm_key = (layer_def.typexy, layer_def.symm)
        symmetric_blocks.extend(typexy_and_symm_to_fun[typexy_symm_key](layer_blocks))

    return symmetric_blocks


def handle_symmetry_31(layer_blocks) -> list:
    """
    The option 31 is intended for two-in-one window frame dipoles with the apertures atop each other.
    :param layer_blocks:
    :return:
    """
    rotated_blocks = [layer_block.rotate(180) for layer_block in layer_blocks]
    mirrored_blocks = [rotated_block.mirror_x() for rotated_block in layer_blocks + rotated_blocks]
    negated_mirrored_blocks = [mirrored_block.negate_current()
                               for mirrored_block in mirrored_blocks]
    return negated_mirrored_blocks + rotated_blocks


def handle_symmetry_33(layer_blocks) -> list:
    """
    The 33-option however, is designed for a single-aperture window frame quadrupole.
    :param layer_blocks:
    :return:
    """
    rotated_blocks = [layer_block.rotate(90).mirror_y() for layer_block in layer_blocks]
    mirrored_y_blocks = [rotated_block.mirror_y().negate_current() for rotated_block in layer_blocks + rotated_blocks]
    mirror_x_blocks = [mirrored_y_block.mirror_x().negate_current()
                       for mirrored_y_block in layer_blocks + rotated_blocks + mirrored_y_blocks]
    return mirror_x_blocks + mirrored_y_blocks + rotated_blocks


def handle_symmetry_41(layer_blocks) -> list:
    """
    The option 41 yields the blocks in the upper half-plane for solenoid calculations.
    :param layer_blocks:
    :return:
    """
    mirrored_y_blocks = [rotated_block.mirror_y() for rotated_block in layer_blocks]
    return layer_blocks + mirrored_y_blocks


def handle_symmetry_type_42(layer_blocks) -> list:
    """
    The 33-option however, is designed for a single-aperture window frame quadrupole.
    :param layer_blocks:
    :return:
    """
    return [layer_block.mirror_x() for layer_block in layer_blocks]


def handle_one_coil_symmetry_2_4_6_8_10_12(layer_blocks, symm):
    angle = 360 * (1 - 1 / symm)
    rotated_blocks = [layer_block.rotate(angle) for layer_block in layer_blocks]
    mirrored_blocks = [rotated_block.mirror_x() for rotated_block in rotated_blocks]
    return [mirrored_block.negate_current() for mirrored_block in mirrored_blocks]


def handle_all_symmetry_2_4_6_8_10_12(layer_blocks, symm) -> list:
    """

    2 - Dipole
    4 - Quadrupole
    6 - Sextupole
    8 - Octupole
    10 - Decapole
    12 - Dodecapole

    :param layer_blocks:
    :param symm:
    :return:
    """
    rotated_blocks = rotate_blocks_and_change_current_sign(layer_blocks, symm)
    mirrored_blocks = [rotated_block.mirror_x() for rotated_block in layer_blocks + rotated_blocks]
    return mirrored_blocks + rotated_blocks


def handle_connection_side_2_4_6_8_10_12(layer_blocks, symm) -> list:
    """

    :param layer_blocks:
    :param symm:
    :return:
    """
    return rotate_blocks_and_change_current_sign(layer_blocks, symm)


def rotate_blocks_and_change_current_sign(layer_blocks, symmetry_type) -> list:
    prev_blocks = layer_blocks
    rotated_blocks = []
    for i in range(symmetry_type - 1):
        angle = 360 / symmetry_type
        temp_rotated_blocks = [prev_block.rotate(angle) for prev_block in prev_blocks]

        temp_rotated_blocks = [temp_rotated_block.negate_current()
                               for temp_rotated_block in temp_rotated_blocks]

        prev_blocks = deepcopy(temp_rotated_blocks)
        rotated_blocks.extend(temp_rotated_blocks)

    return rotated_blocks
