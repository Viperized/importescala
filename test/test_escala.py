import unittest
import sys
from datetime import datetime
from datetime import time

from escala import Escala
import dirs

dirs.default_dir = dirs.TestDir()

class FrameTest(unittest.TestCase):

    def setUp(self):
        self.escala = Escala('fixtures/escala.xml')
        self.dir = dirs.TestDir()
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_AttributosVoo1(self):
        p_voo = self.escala.escalas[0]

        self.assertEqual(p_voo.activity_date,datetime(2013,3,1,11,36))
        self.assertEqual(p_voo.present_location, 'VCP')
        self.assertEqual(p_voo.flight_no, '4148')
        self.assertEqual(p_voo.origin, 'VCP')
        self.assertEqual(p_voo.destination, 'GYN')
        self.assertEqual(p_voo.actype, 'E95')
        self.assertTrue(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, datetime(2013,3,1,10,36))
        self.assertEqual(p_voo.std, datetime(2013,3,1,13,13))
        self.assertEqual(p_voo.sta, datetime(2013,3,1,11,36))
        self.assertEqual(p_voo.activity_info, 'AD4148')
        self.assertFalse(p_voo.duty_design)

    def test_AttributosVoo17(self):
        p_voo = self.escala.escalas[17]

        self.assertEqual(p_voo.activity_date,datetime(2013,10,28,3,0))
        self.assertEqual(p_voo.present_location, 'VCP')
        self.assertEqual(p_voo.flight_no, None)
        self.assertEqual(p_voo.origin, 'VCP')
        self.assertEqual(p_voo.destination, 'VCP')
        self.assertEqual(p_voo.activity_info, 'P04')
        self.assertEqual(p_voo.actype, None)
        self.assertEqual(p_voo.sta, datetime(2013,10,28,3,0))
        self.assertEqual(p_voo.std, datetime(2013,10,28,15,0))
        self.assertFalse(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, None)
        self.assertFalse(p_voo.duty_design)

    def test_AttributosVoo18(self):
        p_voo = self.escala.escalas[18]

        self.assertEqual(p_voo.activity_date,datetime(2013,10,29,4,58))
        self.assertEqual(p_voo.present_location, 'VCP')
        self.assertEqual(p_voo.flight_no, '4050')
        self.assertEqual(p_voo.origin, 'VCP')
        self.assertEqual(p_voo.destination, 'FLN')
        self.assertEqual(p_voo.activity_info, 'AD4050')
        self.assertEqual(p_voo.actype, 'E95')
        self.assertEqual(p_voo.sta, datetime(2013,10,29,4,58))
        self.assertEqual(p_voo.std, datetime(2013,10,29,6,15))
        self.assertTrue(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, datetime(2013,10,29,5,8))
        self.assertFalse(p_voo.duty_design)
        self.assertEqual(p_voo.horas_de_voo, '1:17')

    def test_AttributosQuartoVoo(self):
        p_voo = self.escala.escalas[4]
        self.assertFalse(p_voo.checkin)
        self.assertEqual(p_voo.checkin_time, None)
        self.assertEqual(p_voo.flight_no,None)
        self.assertEqual(p_voo.activity_info, 'FR')

    def test_CalculoHorasVoadas(self):
        self.assertEqual(self.escala.soma_horas(), ['4:10', '6:47', '10:57',
                                                    '0:00'])
    def test_NumerosVoos(self):
        self.assertEqual(self.escala.get_numero_voos(), 23)

    def test_ICS(self):
        """
        Check ICS output
        """
        escala = Escala('fixtures/escala_ics.xml')
        f = open(self.dir.get_data_dir()+'fixtures/escala.ics')
        self.assertEqual(escala.ics().split('\n'), f.read().split('\n')[:-1])
        f.close()

    # test_ICS()

    def test_CSV(self):
        check_output = '\
Subject,Start Date,Start Time,End Date,End Time,All Day Event,Location,Description\n\
CheckIn,01/03/2013,10:36,01/03/2013,10:36,False,"Aeroporto Internacional Viracopos",-\n\
Voo VCP-GYN AD4148,01/03/2013,11:36,01/03/2013,13:13,False,"Aeroporto Internacional Viracopos",Horas de voo: 1:37\n\
Voo GYN-PMW AD4298,01/03/2013,23:45,02/03/2013,01:55,False,"Aeroporto Santa Genoveva",Horas de voo: 2:10\n\
CheckIn,01/04/2013,12:28,01/04/2013,12:28,False,"Aeroporto Internacional Tancredo Neves",-\n\
Voo CNF-VCP AD4049 (P),01/04/2013,13:13,01/04/2013,14:28,False,"Aeroporto Internacional Tancredo Neves",Horas de voo: 1:15\n\
FR,02/04/2013,03:15,02/04/2013,03:15,False,,-\n\
FR,03/04/2013,03:15,03/04/2013,03:15,False,,-\n\
REU,08/04/2013,13:40,08/04/2013,17:00,False,,-\n\
Voo GYN-PMW AD4035,05/08/2013,21:15,05/08/2013,22:55,False,"Aeroporto Santa Genoveva",Horas de voo: 1:40\n\
Reserva(R08),04/09/2013,08:16,04/09/2013,14:15,False,,-\n\
Reserva(R04),05/09/2013,04:46,05/09/2013,08:45,False,,-\n\
SobreAviso,08/09/2013,11:00,08/09/2013,23:00,False,,-\n\
Reserva(RHC),09/09/2013,10:00,09/09/2013,14:00,False,,-\n\
SobreAviso,09/10/2013,10:00,09/10/2013,14:00,False,,-\n\
Simulador (S04),09/11/2013,10:00,09/11/2013,14:00,False,,-\n\
Reserva(R0),09/12/2013,05:00,09/12/2013,12:00,False,,-\n\
Reserva(R07),26/10/2013,06:15,26/10/2013,09:30,False,,-\n\
FP,06/10/2013,06:50,06/10/2013,06:50,False,,-\n\
Reserva(R12),25/10/2013,11:00,25/10/2013,16:00,False,,-\n\
SobreAviso,28/10/2013,03:00,28/10/2013,15:00,False,,-\n\
CheckIn,29/10/2013,05:08,29/10/2013,05:08,False,"Aeroporto Internacional Viracopos",-\n\
Voo VCP-FLN AD4050,29/10/2013,04:58,29/10/2013,06:15,False,"Aeroporto Internacional Viracopos",Horas de voo: 1:17\n\
CheckIn,29/10/2013,05:08,29/10/2013,05:08,False,"Aeroporto Internacional Viracopos",-\n\
Voo VCP-FLN AD4050,29/10/2013,16:05,29/10/2013,20:18,False,"Aeroporto Internacional Viracopos",Horas de voo: 4:13\n\
F,30/10/2013,06:50,30/10/2013,06:50,False,,-\n\
FA,30/10/2013,06:50,30/10/2013,06:50,False,,-\n\
SobreAviso,01/11/2013,03:00,01/11/2013,15:00,False,,-\n\
Simulador (S18),30/01/2017,18:00,30/01/2017,22:00,False,"Aeroporto Internacional Viracopos",Horas de voo: 4:00\n'

        self.assertEqual(self.escala.csv(), check_output)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
