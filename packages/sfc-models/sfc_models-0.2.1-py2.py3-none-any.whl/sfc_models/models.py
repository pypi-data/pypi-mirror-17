"""
models.py
==========


Core classes for machine-generated equations.

Copyright 2016 Brian Romanchuk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from pprint import pprint
import traceback

from sfc_models.utils import LogicError, replace_token_from_lookup, create_equation_from_terms
import sfc_models.iterative_machine_generator as iterative_machine_generator


class Entity(object):
    """
    Entity class
    Base class for all model entities. Gives them a unique numeric id to make debugging easier.

    Can create function for displaying, etc.
    """
    ID = 0

    def __init__(self, parent=None):
        self.ID = Entity.ID
        Entity.ID += 1
        self.Parent = parent
        self.Code = ''
        self.LongName = ''


class Model(Entity):
    """
    Model class.
    All other entities live within a model.


    """

    def __init__(self):
        Entity.__init__(self)
        self.CountryList = []
        self.Exogenous = []
        self.FinalEquations = '<To be generated>'

    def main(self, base_file_name=None):  # pragma: no cover
        """
        Builds model, once all sector and exogenous definitions are in place.
        :return: str
        """
        # Excluded from unit test coverage for now. The components are all tested; this function is really a
        # end-to-end test. Only include in coverage once output file format is finalised.
        if base_file_name is not None:
            log_file = base_file_name + '_log.txt'
        else:
            log_file = None
        try:
            self.GenerateFullSectorCodes()
            self.GenerateEquations()
            self.GenerateIncomeEquations()
            self.ProcessExogenous()
            self.FinalEquations = self.CreateFinalEquations()
            if base_file_name is not None:
                model_file = base_file_name + '.py'
                obj = iterative_machine_generator.IterativeMachineGenerator(self.FinalEquations)
                obj.main(model_file)
                self.LogInfo(log_file)
        except Exception as e:
            self.LogInfo(log_file, e)
            raise
        return self.FinalEquations

    def AddExogenous(self, sector_fullcode, varname, value):
        """
        Add an exogenous variable to the model. Overwrites an existing variable definition.
        Need to use the full sector code.

        :param sector_fullcode: str
        :param varname: str
        :param value: str
        :return:
        """
        self.Exogenous.append((sector_fullcode, varname, value))

    def LogInfo(self, file_name, generate_full_codes=True, ex=None):  # pragma: no cover
        """
        Write information to a file; if there is an exception, dump the trace.
        The log will normally generate the full sector codes; set generate_full_codes=False
        to leave the Model full codes untouched.

        :param file_name: str
        :param generate_full_codes: bool
        :param ex: Exception
        :return:
        """
        # Not covered with unit tests [for now]. Output format will change a lot.
        if file_name is None:
            return
        if generate_full_codes:
            self.GenerateFullSectorCodes()
        with open(file_name, 'w') as f:
            for c in self.CountryList:
                f.write('Country: Code= "%s" %s\n' % (c.Code, c.LongName))
                f.write('='*60 + '\n\n')
                for s in c.SectorList:
                    f.write(s.Dump() + '\n')
            f.write('\n\nFinal Equations:\n')
            f.write(self.FinalEquations + '\n')
            if ex is not None:
                f.write('\n\nError raised:\n')
                traceback.print_exc(file=f)



    def AddCountry(self, country):
        """
        Add a country to the list.
        :param country: Country
        :return: None
        """
        self.CountryList.append(country)

    def GenerateFullSectorCodes(self):
        """
        Create full sector names (which is equal to '[country.Code]_[sector.Code]' - if there is more than one country.
        Equals the sector code otherwise.
        :return: None
        """
        add_country_code = len(self.CountryList) > 1
        for cntry in self.CountryList:
            for sector in cntry.SectorList:
                if add_country_code:
                    sector.FullCode = cntry.Code + '_' + sector.Code
                else:
                    sector.FullCode = sector.Code

    def LookupSector(self, fullcode):
        for cntry in self.CountryList:
            try:
                s = cntry.LookupSector(fullcode, is_full_code=True)
                return s
            except KeyError:
                pass
        raise KeyError('Sector with FullCode does not exist: ' + fullcode)

    def ProcessExogenous(self):
        for sector_code, varname, eqn in self.Exogenous:
            sector = self.LookupSector(sector_code)
            if varname not in sector.Equations:
                raise KeyError('Sector %s does not have variable %s' % (sector_code, varname))
            # Need to mark exogenous variables
            sector.Equations[varname] = 'EXOGENOUS ' + eqn

    def GenerateEquations(self):
        for cntry in self.CountryList:
            for sector in cntry.SectorList:
                sector.GenerateEquations()

    def DumpEquations(self):
        out = ''
        for cntry in self.CountryList:
            for sector in cntry.SectorList:
                out += sector.Dump()
        return out

    def GenerateIncomeEquations(self):
        for cntry in self.CountryList:
            for sector in cntry.SectorList:
                sector.GenerateIncomeEquations()

    def CreateFinalEquations(self):
        """
        Create Final equations.

        Final output, which is a text block of equations
        :return: str
        """
        out = []
        for cntry in self.CountryList:
            for sector in cntry.SectorList:
                out.extend(sector.CreateFinalEquations())
        return self.FinalEquationFormatting(out)

    @staticmethod
    def FinalEquationFormatting(out):
        endo = []
        exo = []
        for row in out:
            if 'EXOGENOUS' in row[1]:
                new_eqn = row[1].replace('EXOGENOUS', '')
                exo.append((row[0], new_eqn, row[2]))
            else:
                endo.append(row)
        max0 = max([len(x[0]) for x in out])
        max1 = max([len(x[1]) for x in out])
        formatter = '%<max0>s = %-<max1>s  # %s'
        formatter = formatter.replace('<max0>', str(max0))
        formatter = formatter.replace('<max1>', str(max1))
        endo = [formatter % x for x in endo]
        exo = [formatter % x for x in exo]
        s = '\n'.join(endo) + '\n\n# Exogenous Variables\n\n' + '\n'.join(exo)
        s += '\n\nMaxTime = 100\nErr_Tolerance=0.001'
        return s


class Country(Entity):
    """
    Country class. Somewhat redundant in a closed economy model, but we need for multi-region models.
    """

    def __init__(self, model, long_name, code):
        Entity.__init__(self, model)
        self.Code = code
        self.LongName = long_name
        model.AddCountry(self)
        self.SectorList = []

    def AddSector(self, sector):
        self.SectorList.append(sector)

    def LookupSector(self, code, is_full_code=False):
        """
        Get the sector object via code or fullcode
        :param code: str
        :param is_full_code: bool
        :return: Sector
        """
        if is_full_code:
            for s in self.SectorList:
                if s.FullCode == code:
                    return s
        else:
            for s in self.SectorList:
                if s.Code == code:
                    return s
        raise KeyError('Sector does not exist - ' + code)


class Sector(Entity):
    """
    All sectors derive from this class.
    """

    def __init__(self, country, long_name, code):
        Entity.__init__(self, country)
        country.AddSector(self)
        self.Code = code
        # This is calculated by the Model
        self.FullCode = ''
        self.LongName = long_name
        self.VariableDescription = {}
        self.Equations = {}
        self.AddVariable('F', 'Financial assets', '<TO BE GENERATED>')
        self.AddVariable('LAG_F', 'Previous period''s financial assets.', 'F(k-1)')
        self.CashFlows = []

    def AddVariable(self, varname, desc, eqn):
        self.VariableDescription[varname] = desc
        self.Equations[varname] = eqn

    def GetVariables(self):
        """
        Return a sorted list of variables.

        (Need to sort to make testing easier; dict's store in "random" hash order.
        :return: list
        """
        variables = list(self.Equations.keys())
        variables.sort()
        return variables

    def GetVariableName(self, varname):
        """

        :param varname: str
        :return: str
        """
        if self.FullCode == '':
            raise LogicError('Must generate FullCode before calling GetVariableName')
        if varname not in self.Equations:
            raise KeyError('Variable %s not in sector %s' % (varname, self.FullCode))
        return self.FullCode + '_' + varname

    def AddCashFlow(self, term, eqn, desc):
        term = term.strip()
        if len(term) == 0:
            return
        term = term.replace(' ', '')
        if not (term[0] in ('+', '-')):
            term = '+' + term
        if len(term) < 2:
            raise ValueError('Invalid cash flow term')
        self.CashFlows.append(term)
        # Remove the +/- from the term
        term = term[1:]
        if term in self.Equations:
            if len(self.Equations[term]) == 0:
                self.Equations[term] = eqn
        else:
            self.AddVariable(term, desc, eqn)

    def GenerateEquations(self):
        return

    def Dump(self):
        out = '[%s] %s. FullCode = "%s" \n' % (self.Code, self.LongName, self.FullCode)
        out += '-' * 60 + '\n'
        for var in self.Equations:
            out += '%s = %s\n' % (var, self.Equations[var])
        return out

    def GenerateIncomeEquations(self):
        if len(self.CashFlows) == 0:
            self.Equations['F'] = ''
            self.Equations['LAG_F'] = ''
            return
        self.CashFlows = ['LAG_F', ] + self.CashFlows
        eqn = create_equation_from_terms(self.CashFlows)
        self.Equations['F'] = eqn

    def CreateFinalEquations(self):
        out = []
        lookup = {}
        for varname in self.Equations:
            lookup[varname] = self.GetVariableName(varname)
        # Use GetVariables() so that we re always sorted; needed for unit tests
        for varname in self.GetVariables():
            if len(self.Equations[varname].strip()) == 0:
                continue
            out.append((self.GetVariableName(varname),
                        replace_token_from_lookup(self.Equations[varname], lookup),
                        '[%s] %s' % (varname, self.VariableDescription[varname])))
        return out


class Market(Sector):
    """
    Market Not really a sector, but keep it in the same list
    """

    def __init__(self, country, long_name, code):
        Sector.__init__(self, country, long_name, code)
        self.NumSupply = 0

    def GenerateEquations(self):
        self.NumSupply = 0
        self.GenerateTermsLowLevel('SUP', 'Supply')
        if self.NumSupply == 0:
            raise ValueError('No supply for market: ' + self.FullCode)
        if self.NumSupply > 1:
            raise NotImplementedError('More than one supply for a market is not yet supported: ' + self.Code)
        self.GenerateTermsLowLevel('DEM', 'Demand')
        if self.NumSupply == 1:
            self.FixSingleSupply()

    def GenerateTermsLowLevel(self, prefix, long_desc):
        if prefix not in ('SUP', 'DEM'):
            raise LogicError('Input to function must be "SUP" or "DEM"')
        country = self.Parent
        var_name = prefix + '_' + self.Code
        self.AddVariable(var_name, long_desc + ' for Market ' + self.Code, '')
        term_list = []
        for s in country.SectorList:
            if s.ID == self.ID:
                continue
            try:
                term = s.GetVariableName(var_name)
            except KeyError:
                continue
            term_list.append('+ ' + term)
            if prefix == 'SUP':
                # Since we assume that there is a single supplier, we can set the supply equation to
                # point to the equation in the market.
                s.AddCashFlow(var_name, self.GetVariableName(var_name), long_desc)
                self.NumSupply += 1
            else:
                # Must fill in demand equation in sectors.
                s.AddCashFlow('-' + var_name, 'Error: must fill in demand equation', long_desc)
        eqn = create_equation_from_terms(term_list)
        self.Equations[var_name] = eqn

    def FixSingleSupply(self):
        if self.NumSupply != 1:
            raise LogicError('Can only call this function with a single supply source!')
        country = self.Parent
        sup_name = 'SUP_' + self.Code
        dem_name = 'DEM_' + self.Code
        self.Equations[sup_name] = dem_name
        for s in country.SectorList:
            if s.ID == self.ID:
                continue
            if sup_name in s.Equations:
                s.Equations[sup_name] = self.Equations[dem_name]
                return
