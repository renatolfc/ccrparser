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
    '''
    <div class="box_pontos">
      <h3 class="titulo_principal">SENTIDO: Pista Rio-SP</h3>
      <div class="box_postos">
          <p>
          </p>
      </div>
    </div>
    ''',
    '',
    '''
    <div class="box_pontos">
      <h3 class="titulo_principal">SENTIDO: Pista SP-Rio</h3>
      <div class="box_postos">
          <p>
            <strong>Lugar 1</strong><br />
            Condições de Tráfego: bla bla bla<br />
            Pista: 1<br />
            Motivo: 2<br />
            Observação: 3<br />
            KM Inicial: 4<br />
            KM Final: <br />
            <br />
          </p>
      </div>
    </div>
    ''',
    '''
    <div class="box_pontos">
      <h3 class="titulo_principal">SENTIDO: Pista SP-Rio</h3>
      <div class="box_postos">
          <p>
            <strong>Lugar 1</strong><br />
            Condições de Tráfego:<br />
            Pista:<br />
            Motivo:<br />
            Observação: 1<br />
            KM Inicial:<br />
            KM Final: 1<br />
            <br />
          </p>
      </div>
    </div>
    ''',
    '''
    <div class="box_pontos">
      <h3 class="titulo_principal">SENTIDO: Pista SP-Rio</h3>
      <div class="box_postos">
          <p>
            <strong>Lugar 1</strong><br />
            Condições de Tráfego:1<br />
            Pista:1<br />
            Motivo:1<br />
            Observação:1<br />
            KM Inicial:1<br />
            KM Final:1<br />
            <br />
          </p>
      </div>
    </div>
    ''',
    '''
    <div class="box_pontos">
      <h3 class="titulo_principal">SENTIDO: Interior/Capital (Sul)</h3>
      <div class="box_postos">
          <p>
            <strong>Bandeirantes - Trecho: São Paulo - Jundiaí</strong><br />
            Condições de Tráfego: Congestionado<br />
            Pista: Expressa<br />
            Motivo: Acidente<br />
            Observação: Ás 21:25 faixa 1 liberada.
    ás 21:43 faixa 2 liberadas.<br />
            KM Inicial: <span class='km'>55</span><br />
            KM Final: <span class='km'>51</span><br />
            Trecho: Região de Jundiaí.<br />
          </p>
      </div>
    </div>
    <div class="box_pontos">
      <h3 class="titulo_principal">SENTIDO: Interior/Capital (Sul)</h3>
      <div class="box_postos">
          <p>
            <strong>Anhanguera - Trecho: São Paulo - Jundiaí</strong><br />
            Condições de Tráfego: Congestionado<br />
            Pista: Expressa<br />
            Motivo: Acidente<br />
            Observação: <br />
            KM Inicial: <span class='km'>25</span><br />
            KM Final: <span class='km'>25</span><br />
            Trecho: Região de Perus.<br />
          </p>
      </div>
    </div>
    ''',
]

outputMatches = [
    [{u'lane': u'Expressa', u'end': u'150', u'observation': u'Em S\xe3o Jos\xe9 dos Campos.', u'stretch': u'Jacarei - SJCampos km 162 ao 133', u'start': u'149', u'reason': u'Acidente', u'traffic': u'Lento'}],
    [{u'lane': u'Expressa', u'end': u'150', u'observation': u'Em S\xe3o Jos\xe9 dos Campos.', u'stretch': u'Jacarei - SJCampos km 162 ao 133', u'start': u'149', u'reason': u'Acidente', u'traffic': u'Lento'}, {u'lane': u'Local', u'end': u'150', u'observation': u'Em sao trevas.', u'stretch': u'Lugar 1', u'start': u'204', u'reason': u'Acidente', u'traffic': u'Muito rapido'}],
    [{u'lane': u'Expressa', u'end': u'150', u'observation': u'Em S\xe3o Jos\xe9 dos Campos.', u'stretch': u'Jacarei - SJCampos km 162 ao 133', u'start': u'149', u'reason': u'Acidente', u'traffic': u'Lento'}, {u'lane': u'Local', u'end': u'150', u'observation': u'Em sao trevas.', u'stretch': u'Lugar 1', u'start': u'204', u'reason': u'Acidente', u'traffic': u'Muito rapido'}],
    [],
    [],
    [],
    [],
    [{u'lane': u'1', u'end': u'1', u'observation': u'1', u'stretch': u'Lugar 1', u'start': u'1', u'reason': u'1', u'traffic': u'1'}],
    [{u'lane': u'Expressa', u'end': u'25', u'observation': u'-', u'stretch': u'Anhanguera - Trecho: S\xe3o Paulo - Jundia\xed', u'start': u'25', u'reason': u'Acidente', u'traffic': u'Congestionado'}, {u'lane': u'Expressa', u'end': u'51', u'observation': u'\xc1s 21:25 faixa 1 liberada.\n    \xe1s 21:43 faixa 2 liberadas.', u'stretch': u'Bandeirantes - Trecho: S\xe3o Paulo - Jundia\xed', u'start': u'55', u'reason': u'Acidente', u'traffic': u'Congestionado'}],
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
            self.assertEqual(sorted(j), sorted(out))

if __name__ == '__main__':
    unittest.main()

