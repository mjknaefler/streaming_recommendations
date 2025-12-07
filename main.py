# streaming recommendations app

from controllers.main_controller import MainController

def main():
    print("=" * 50)
    print("Streaming Recommendations")
    print("=" * 50)
    
    controller = MainController()
    controller.run()

if __name__ == '__main__':
    main()
