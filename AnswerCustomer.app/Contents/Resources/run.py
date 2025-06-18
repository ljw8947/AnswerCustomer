from app import create_app
import argparse

app = create_app()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AnswerCustomer Flask应用')
    parser.add_argument('--port', type=int, default=5000, help='服务器端口 (默认: 5000)')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='服务器主机 (默认: 127.0.0.1)')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    
    args = parser.parse_args()
    
    print(f"🚀 启动AnswerCustomer服务器...")
    print(f"   地址: http://{args.host}:{args.port}")
    print(f"   调试模式: {'开启' if args.debug else '关闭'}")
    print("   💡 按 Ctrl+C 停止服务器")
    print("-" * 50)
    
    app.run(host=args.host, port=args.port, debug=args.debug) 