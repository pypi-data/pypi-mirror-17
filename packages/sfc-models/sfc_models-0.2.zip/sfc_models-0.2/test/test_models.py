from unittest import TestCase

from sfc_models.models import *
from sfc_models.sectors import Household, DoNothingGovernment


class TestEntity(TestCase):
    def test_ctor(self):
        Entity.ID = 0
        a = Entity()
        self.assertEqual(a.ID, 0)
        b = Entity(a)
        self.assertEqual(b.ID, 1)
        self.assertEqual(b.Parent.ID, 0)


class Stub(object):
    """
    Use the stub_fun to count how many times a method has been called.
    Used for testing the iteration in the Model class; the output depends upon the sector,
    which are tested separately.
    """

    def __init__(self):
        self.Count = 0

    def stub_fun(self):
        self.Count += 1

    def stub_return(self):
        self.Count += 1
        return [(str(self.Count), 'a', 'b')]


class TestModel(TestCase):
    def test_GenerateFullCodes_1(self):
        mod = Model()
        country = Country(mod, 'USA!', 'US')
        household = Sector(country, 'Household', 'HH')
        mod.GenerateFullSectorCodes()
        self.assertEqual(household.FullCode, 'HH')

    def test_GenerateFullCodes_2(self):
        mod = Model()
        us = Country(mod, 'USA', 'US')
        can = Country(mod, 'Canada', 'Eh?')
        household = Sector(us, 'Household', 'HH')
        can_hh = Sector(can, 'Household', 'HH')
        mod.GenerateFullSectorCodes()
        self.assertEqual(household.FullCode, 'US_HH')
        self.assertEqual(can_hh.FullCode, 'Eh?_HH')

    def test_LookupSector(self):
        mod = Model()
        us = Country(mod, 'USA', 'US')
        can = Country(mod, 'Canada', 'Eh?')
        household = Sector(us, 'Household', 'HH')
        can_hh = Sector(can, 'Household', 'HH')
        mod.GenerateFullSectorCodes()
        self.assertEqual(household, mod.LookupSector('US_HH'))
        self.assertEqual(can_hh, mod.LookupSector('Eh?_HH'))
        with self.assertRaises(KeyError):
            mod.LookupSector('HH')

    def test_ForceExogenous(self):
        mod = Model()
        us = Country(mod, 'USA', 'US')
        household = Sector(us, 'Household', 'HH')
        mod.GenerateFullSectorCodes()
        mod.Exogenous = [('HH', 'F', 'TEST')]
        mod.ForceExogenous()
        self.assertEqual('EXOGENOUS TEST', household.Equations['F'])

    def test_ForceExogenous2(self):
        mod = Model()
        us = Country(mod, 'USA', 'US')
        household = Sector(us, 'Household', 'HH')
        mod.GenerateFullSectorCodes()
        mod.Exogenous = [('HH', 'Foo', 'TEST')]
        with self.assertRaises(KeyError):
            mod.ForceExogenous()

    def test_GenerateEquations(self):
        # Just count the number if times the stub is called
        stub = Stub()
        mod = Model()
        us = Country(mod, 'USA', 'US')
        h1 = Sector(us, 'Household', 'HH')
        h2 = Sector(us, 'Capitalists', 'CAP')
        h1.GenerateEquations = stub.stub_fun
        h2.GenerateEquations = stub.stub_fun
        mod.GenerateEquations()
        self.assertEqual(2, stub.Count)

    def test_GenerateIncomeEquations(self):
        stub = Stub()
        mod = Model()
        us = Country(mod, 'USA', 'US')
        h1 = Sector(us, 'Household', 'HH')
        h1.GenerateIncomeEquations = stub.stub_fun
        mod.GenerateIncomeEquations()
        self.assertEqual(1, stub.Count)

    def test_CreateFinalFunctions(self):
        stub = Stub()
        mod = Model()
        us = Country(mod, 'USA', 'US')
        h1 = Sector(us, 'Household', 'HH')
        h2 = Sector(us, 'Household2', 'H2')
        h1.CreateFinalEquations = stub.stub_return
        h2.CreateFinalEquations = stub.stub_return
        out = mod.CreateFinalEquations()
        out = out.split('\n')
        self.assertTrue('1' in out[0])
        self.assertTrue('2' in out[1])

    def test_FinalEquationFormating(self):
        eq = [('x', 'y + 1', 'comment_x'),
              ('y', 'EXOGENOUS 20', 'comment_y'),
              ('z', 'd', 'comment_z')]
        out = Model.FinalEquationFormatting(eq)
        # Remove spaces; what matters is the content
        out = out.replace(' ', '').split('\n')
        target = ['x=y+1#comment_x', 'z=d#comment_z', '', '#ExogenousVariables', '', 'y=20#comment_y']
        self.assertEqual(target, out)


class TestSector(TestCase):
    def test_ctor_chain(self):
        mod = Model()
        country = Country(mod, 'USA! USA!', 'US')
        household = Sector(country, 'Household', 'HH')
        self.assertEqual(household.Parent.Code, 'US')
        self.assertEqual(household.Parent.Parent.Code, '')

    def test_GetVariables(self):
        mod = Model()
        can = Country(mod, 'Canada', 'Eh')
        can_hh = Sector(can, 'Household', 'HH')
        can_hh.AddVariable('y', 'Vertical axis', '2.0')
        can_hh.AddVariable('x', 'Horizontal axis', 'y - t')
        self.assertEqual(can_hh.GetVariables(), ['F', 'LAG_F', 'x', 'y'])

    def test_GetVariableName_1(self):
        mod = Model()
        us = Country(mod, 'USA', 'US')
        household = Household(us, 'Household', 'HH', .9, .2)
        mod.GenerateFullSectorCodes()
        household.GenerateEquations()
        self.assertEqual(household.GetVariableName('AlphaFin'), 'HH_AlphaFin')

    def test_GetVariableName_2(self):
        mod = Model()
        us = Country(mod, 'USA', 'US')
        household = Household(us, 'Household', 'HH', .9, .2)
        with self.assertRaises(LogicError):
            household.GetVariableName('AlphaFin')

    def test_GetVariableName_3(self):
        mod = Model()
        us = Country(mod, 'USA', 'US')
        hh = Sector(us, 'Household', 'HH')
        mod.GenerateFullSectorCodes()
        with self.assertRaises(KeyError):
            hh.GetVariableName('Kaboom')

    def test_AddCashFlow(self):
        mod = Model()
        us = Country(mod, 'USA', 'US')
        s = Sector(us, 'Household', 'HH')
        s.AddCashFlow('A', 'H_A', 'Desc A')
        s.AddCashFlow('- B', 'H_B', 'Desc B')
        s.AddCashFlow(' - C', 'H_C', 'Desc C')
        self.assertEqual(['+A', '-B', '-C'], s.CashFlows)

    def test_AddCashFlow_2(self):
        mod = Model()
        us = Country(mod, 'USA', 'US')
        s = Sector(us, 'Household', 'HH')
        s.AddCashFlow('A', 'equation', 'Desc A')
        s.AddCashFlow('', 'equation', 'desc')
        with self.assertRaises(ValueError):
            s.AddCashFlow('-', 'B', 'Desc B')
        with self.assertRaises(ValueError):
            s.AddCashFlow('+', 'X', 'Desc C')
        self.assertEqual(['+A'], s.CashFlows)
        self.assertEqual('equation', s.Equations['A'])

    def test_AddCashFlow_3(self):
        mod = Model()
        us = Country(mod, 'USA', 'US')
        s = Sector(us, 'Household', 'HH')
        s.AddVariable('X', 'desc', '')
        s.AddCashFlow('X', 'equation', 'Desc A')
        self.assertEqual('equation', s.Equations['X'])

    def test_GenerateIncomeEquations(self):
        mod = Model()
        us = Country(mod, 'USA', 'US')
        s = Sector(us, 'Household', 'HH')
        s.GenerateIncomeEquations()
        self.assertEqual('', s.Equations['F'])
        self.assertEqual('', s.Equations['LAG_F'])

    def test_GenerateIncomeEquations_2(self):
        mod = Model()
        us = Country(mod, 'USA', 'US')
        s = Sector(us, 'Household', 'HH')
        s.CashFlows.append('X')
        s.GenerateIncomeEquations()
        self.assertEqual('LAG_F+X', s.Equations['F'])
        self.assertEqual('F(k-1)', s.Equations['LAG_F'])

    def test_GenerateIncomeEquations_3(self):
        mod = Model()
        us = Country(mod, 'USA', 'US')
        s = Sector(us, 'Household', 'HH')
        s.CashFlows.append('X')
        s.CashFlows.append('Y')
        s.GenerateIncomeEquations()
        self.assertEqual('LAG_F+X+Y', s.Equations['F'])
        self.assertEqual('F(k-1)', s.Equations['LAG_F'])

    def test_GenerateFinalEquations(self):
        mod = Model()
        us = Country(mod, 'USA', 'US')
        s = Sector(us, 'Household', 'HH')
        mod.GenerateFullSectorCodes()
        s.Equations = {'F': '', 'X': 't+1', 'Y': 'X+1'}
        s.VariableDescription = {'F': 'DESC F', 'X': 'DESC X', 'Y': 'DESC Y'}
        out = s.CreateFinalEquations()
        # Since F has an empty equation, does not appear.
        targ = [('HH_X', 't+1', '[X] DESC X'), ('HH_Y', 'HH_X+1', '[Y] DESC Y')]
        # Kill spacing in equations
        out = [(x[0], x[1].replace(' ', ''), x[2]) for x in out]
        self.assertEqual(targ, out)


class TestCountry(TestCase):
    def test_AddSector(self):
        mod = Model()
        can = Country(mod, 'Canada', 'Eh')
        gov = DoNothingGovernment(can, 'Government', 'GOV')
        self.assertEqual(can.SectorList[0].ID, gov.ID)

    def test_LookupSector(self):
        mod = Model()
        can = Country(mod, 'Canada', 'Eh')
        gov = DoNothingGovernment(can, 'Government', 'GOV')
        hh = Household(can, 'Household', 'HH', .9, .2)
        self.assertEqual(can.LookupSector('HH').ID, hh.ID)
        self.assertEqual(can.LookupSector('GOV').ID, gov.ID)
        with self.assertRaises(KeyError):
            can.LookupSector('Smurf')


class TestMarket(TestCase):
    def test_GenerateEquations(self):
        mod = Model()
        can = Country(mod, 'Canada', 'Eh')
        mar = Market(can, 'Market', 'LAB')
        bus = Sector(can, 'Business', 'BUS')
        hh = Sector(can, 'Household', 'HH')
        bus.AddVariable('DEM_LAB', 'desc', 'x')
        hh.AddVariable('SUP_LAB', 'desc 2', '')
        mod.GenerateFullSectorCodes()
        mar.GenerateEquations()
        self.assertEqual(['-DEM_LAB', ], bus.CashFlows)
        self.assertEqual('x', bus.Equations['DEM_LAB'])
        self.assertEqual(['+SUP_LAB', ], hh.CashFlows)
        self.assertEqual('BUS_DEM_LAB', hh.Equations['SUP_LAB'].strip())

    def test_GenerateEquations_no_supply(self):
        mod = Model()
        can = Country(mod, 'Canada', 'Eh')
        mar = Market(can, 'Market', 'LAB')
        bus = Sector(can, 'Business', 'BUS')
        bus.AddVariable('DEM_LAB', 'desc', '')
        mod.GenerateFullSectorCodes()
        with self.assertRaises(ValueError):
            mar.GenerateEquations()

    def test_GenerateEquations_2_supply(self):
        mod = Model()
        can = Country(mod, 'Canada', 'Eh')
        mar = Market(can, 'Market', 'LAB')
        bus = Sector(can, 'Business', 'BUS')
        hh = Sector(can, 'Household', 'HH')
        hh2 = Sector(can, 'Household', 'HH2')
        bus.AddVariable('DEM_LAB', 'desc', 'x')
        hh.AddVariable('SUP_LAB', 'desc 2', '')
        hh2.AddVariable('SUP_LAB', 'desc 2', '')
        mod.GenerateFullSectorCodes()
        with self.assertRaises(NotImplementedError):
            mar.GenerateEquations()

    def test_GenerateTermsLowLevel(self):
        mod = Model()
        can = Country(mod, 'Canada', 'Eh')
        mar = Market(can, 'Market', 'LAB')
        bus = Sector(can, 'Business', 'BUS')
        bus.AddVariable('DEM_LAB', 'desc', '')
        mod.GenerateFullSectorCodes()
        mar.GenerateTermsLowLevel('DEM', 'Demand')
        self.assertEqual(['-DEM_LAB', ], bus.CashFlows)
        self.assertTrue('error' in bus.Equations['DEM_LAB'].lower())


    def test_GenerateTermsLowLevel_3(self):
        mod = Model()
        can = Country(mod, 'Canada', 'Eh')
        mar = Market(can, 'Market', 'LAB')
        with self.assertRaises(LogicError):
            mar.GenerateTermsLowLevel('Blam!', 'desc')

    def test_FixSingleSupply(self):
        mod = Model()
        can = Country(mod, 'Canada', 'Eh')
        mar = Market(can, 'Market', 'LAB')
        with self.assertRaises(LogicError):
            mar.FixSingleSupply()
