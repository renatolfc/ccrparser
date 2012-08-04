#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import unittest
from CCRParser import CCRParser

inputStrs = [
    '''
    <div class="box_pontos">
      <h3 class="titulo_principal">SENTIDO: Pista Rio-SP</h3>
      <div class="box_postos">
          <p>
            <strong>Jacarei - SJCampos km 162 ao 133</strong><br />
            Condições de Tráfego: Lento<br />
            Pista: Expressa<br />
            Motivo: Acidente<br />
            Observação: Em São José dos Campos. <br />
            KM Inicial: <span class='km'>149</span><br />
            KM Final: <span class='km'>150</span><br />
            <br />
          </p>
      </div>
    </div>
    ''',
    '''
    <div class="box_pontos">
      <h3 class="titulo_principal">SENTIDO: Pista Rio-SP</h3>
      <div class="box_postos">
          <p>
            <strong>Jacarei - SJCampos km 162 ao 133</strong><br />
            Condições de Tráfego: Lento<br />
            Pista: Expressa<br />
            Motivo: Acidente<br />
            Observação: Em São José dos Campos. <br />
            KM Inicial: <span class='km'>149</span><br />
            KM Final: <span class='km'>150</span><br />
            <br />
          </p>
      </div>
    </div>
    <div class="box_pontos">
      <h3 class="titulo_principal">SENTIDO: Pista SP-Rio</h3>
      <div class="box_postos">
          <p>
            <strong>Lugar 1</strong><br />
            Condições de Tráfego: Muito rapido<br />
            Pista: Local<br />
            Motivo: Acidente<br />
            Observação: Em sao trevas. <br />
            KM Inicial: <span class='km'>204</span><br />
            KM Final: <span class='km'>150</span><br />
            <br />
          </p>
      </div>
    </div>
    ''',
    '''
    <div class="box_pontos">
      <h3 class="titulo_principal">SENTIDO: Pista Rio-SP</h3>
      <div class="box_postos">
          <p>
            <strong>Jacarei - SJCampos km 162 ao 133</strong><br />
            Condições de Tráfego: Lento<br />
            Pista: Expressa<br />
            Motivo: Acidente<br />
            Observação: Em São José dos Campos. <br />
            KM Inicial: <span class='km'>149</span><br />
            KM Final: <span class='km'>150</span><br />
            <br />
          </p>
          <p>
            <strong>Lugar 1</strong><br />
            Condições de Tráfego: Muito rapido<br />
            Pista: Local<br />
            Motivo: Acidente<br />
            Observação: Em sao trevas. <br />
            KM Inicial: <span class='km'>204</span><br />
            KM Final: <span class='km'>150</span><br />
            <br />
          </p>
      </div>
    </div>
    ''',
]

outputMatches = [
    [{u'lane': u'Expressa', u'end': u'150\n\n', u'observation': u'Em S\xe3o Jos\xe9 dos Campos.', u'stretch': u'\nJacarei - SJCampos km 162 ao 133', u'start': u'149', u'reason': u'Acidente', u'traffic': u'Lento'}],
    [{u'lane': u'Expressa', u'end': u'150\n\n', u'observation': u'Em S\xe3o Jos\xe9 dos Campos.', u'stretch': u'\nJacarei - SJCampos km 162 ao 133', u'start': u'149', u'reason': u'Acidente', u'traffic': u'Lento'}, {u'lane': u'Local', u'end': u'150\n\n', u'observation': u'Em sao trevas.', u'stretch': u'\nLugar 1', u'start': u'204', u'reason': u'Acidente', u'traffic': u'Muito rapido'}],
    [{u'lane': u'Expressa', u'end': u'150\n\n', u'observation': u'Em S\xe3o Jos\xe9 dos Campos.', u'stretch': u'\nJacarei - SJCampos km 162 ao 133', u'start': u'149', u'reason': u'Acidente', u'traffic': u'Lento'}, {u'lane': u'Local', u'end': u'150\n\n', u'observation': u'Em sao trevas.', u'stretch': u'\nLugar 1', u'start': u'204', u'reason': u'Acidente', u'traffic': u'Muito rapido'}],
]

def areMatchesEqual(first, second):
    for i, j in zip(sorted(first), sorted(second)):
        if i != j:
            return False
    return True

class TestCCRParser(unittest.TestCase):
    def setUp(self):
        self.parser = CCRParser()

    def test_parse(self):
        for i, j in zip(inputStrs, outputMatches):
            out = self.parser.parse(i)
            self.assertEqual(sorted(out), sorted(j))

if __name__ == '__main__':
    unittest.main()

