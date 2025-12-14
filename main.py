from MotorDeSimulacao import MotorDeSimulacao

if __name__ == '__main__':
        #motor = MotorDeSimulacao.cria("Parametros_Farol_Fixo")
        motor = MotorDeSimulacao.cria("Parametros_Farol_Aprender")
        #motor = MotorDeSimulacao.cria("Parametros_Farol_Aprender_2")
        #motor = MotorDeSimulacao.cria("Parametros_Farol_Teste")

        #motor = MotorDeSimulacao.cria("Parametros_Lab_Aprender")
        #motor = MotorDeSimulacao.cria("Parametros_Lab_Teste")
        #motor = MotorDeSimulacao.cria("Parametros_Lab_Fixo")

        motor.executa()

