#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Code generator for fortran runtime library
'''

from distutils.dir_util import copy_tree
from pathlib import Path
from typing import Dict

from dmtgen import BaseGenerator, TemplateBasedGenerator
from dmtgen.common.package import Package

from .basic_template_generator import (BasicTemplateGenerator)


class RuntimeGenerator(BaseGenerator):
    """ Generates a fortran runtime library to access the entities as plain objects """

    def __init__(self,root_dir,package_name,output_dir,root_package: Package) -> None:
        super().__init__(root_dir,package_name,output_dir,root_package)

    # def get_template_generators(self) -> Dict[str,TemplateBasedGenerator]:
    #     """ Override in subclasses """
    #     return {
    #     }

    def get_basic_generator(self) -> TemplateBasedGenerator:
        return BasicTemplateGenerator()


    def copy_templates(self, template_root: Path, output_dir: Path):
        """Copy template folder to output folder"""
        if self.source_only:
            src_dir = template_root / "src"
            dest_dir = output_dir
            copy_tree(str(src_dir), str(dest_dir))
        else:
            copy_tree(str(template_root), str(output_dir))
