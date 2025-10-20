from dotenv import load_dotenv

import chess
import openai

load_dotenv()


def print_board_with_coordinates(board):
    board_str = str(board).split('\n')
    print("  a b c d e f g h")
    for i, row in enumerate(board_str):
        print(f"{8 - i} {row} {8 - i}")
    print("  a b c d e f g h\n")


def get_chatgpt_move_with_explanation(board):
    board_fen = board.fen()
    prompt = f"""
        You are a chess-playing assistant.
        Given the current board state in FEN notation,
        respond with only the best move for Black in standard
        algebraic notation on the first line (e.g., e5, Nc6, Qxd5),
        and a brief explanation of the strategic reasoning behind
        the move on the second line.

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
            max_tokens=150
        )
        content = response.choices[0].message.content.strip()
        lines = content.split('\n')
        move = lines[0].strip() if len(lines) > 0 else ""
        explanation = lines[1].strip() if len(
            lines) > 1 else "No explanation provided."
        return move, explanation
    except Exception as e:
        print("Error calling OpenAI API:", e)
        return None, None


def main():
    board = chess.Board()
    print("Welcome to the Chess CLI Agent with Strategy Explanation!")
    print("Enter your moves in standard algebraic notation (e.g., e4, Nf3, Qxd5)")
    print("Type 'exit' to quit.\n")

    while not board.is_game_over():
        print_board_with_coordinates(board)
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
            chatgpt_move, explanation = get_chatgpt_move_with_explanation(
                board)
            print(f"ChatGPT suggests: {chatgpt_move}")
            print(f"Strategy: {explanation}")
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
    print_board_with_coordinates(board)


if __name__ == "__main__":
    main()
