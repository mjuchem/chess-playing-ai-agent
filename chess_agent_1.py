from dotenv import load_dotenv

import chess
import openai

load_dotenv()


def print_board(board):
    print(board)


def get_chatgpt_move(board):
    board_fen = board.fen()
    prompt = f"""
  You are a chess-playing assistant.
  Given the current board state in FEN notation, suggest the best move
  for Black in standard algebraic notation (e.g., e5, Nc6, Qxd5).
  Only respond with the move, nothing else.
  FEN:
  {board_fen}
  """
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful chess-playing assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=10
        )
        move = response.choices[0].message.content.strip()
        return move
    except Exception as e:
        print("Error calling OpenAI API:", e)
        return None


def main():
    board = chess.Board()
    print("Welcome to the Chess CLI Agent with python-chess and ChatGPT!")
    print("Enter your moves in standard algebraic notation (e.g., e4, Nf3, Qxd5)")
    print("Type 'exit' to quit.\n")

    while not board.is_game_over():
        print_board(board)
        if board.turn == chess.WHITE:
            move_input = input("Your move (White): ").strip()
            if move_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            try:
                move = board.parse_san(move_input)
                board.push(move)
            except ValueError:
                print("Invalid move. Please try again.")
        else:
            print("Computer (Black) is thinking...")
            chatgpt_move = get_chatgpt_move(board)
            print(f"ChatGPT suggests: {chatgpt_move}")
            if chatgpt_move:
                try:
                    move = board.parse_san(chatgpt_move)
                    board.push(move)
                    print(f"Computer plays: {chatgpt_move}")
                except ValueError:
                    print("ChatGPT move could not be parsed or is illegal.")
            else:
                print("No move received from ChatGPT.")

    print("Game over.")
    print_board(board)


if __name__ == "__main__":
    main()
