from MotorDeSimulacao import MotorDeSimulacao

if __name__ == '__main__':
        # motor = MotorDeSimulacao.cria("Parametros_Farol_Fixo")
        #motor = MotorDeSimulacao.cria("Parametros_Lab_Fixo")

        #motor_FAROL_SemObstaculos = MotorDeSimulacao.cria("Parametros_Farol_Aprender")
        #motor_FAROL_ComObstaculos = MotorDeSimulacao.cria("Parametros_Farol_Aprender_2")
        motor = MotorDeSimulacao.cria("Parametros_Lab_Aprender")
        #motor = MotorDeSimulacao.cria("Parametros_Lab_Teste")

        motor.executa()
        # motor_FAROL_ComObstacublos.executa()

