# Reversi Pygame Migration

This project contains a Pygame implementation of the Reversi game, migrated from the original GBA (Game Boy Advance) version.

## Project Structure

### Main Files (Root Directory)
- `reversi_pygame.py` - Basic Pygame implementation with simple AI
- `reversi_advanced.py` - Advanced implementation with complete menu system and minimax AI (now with larger display and improved pass/game end logic)
- `requirements.txt` - Python dependencies
- `run_reversi.bat` - Windows batch file launcher with menu selection
- `play_reversi.bat` - Simple Windows batch file to run advanced version
- `run_reversi.ps1` - PowerShell script launcher with better error handling
- `README.md` - This file
- `LICENSE` - MIT License

### GBA Source Code (`gba/` directory)
- Original GBA source files (`.c`, `.h`, `.S`)
- Build artifacts (`.o`, `.gba`, `.elf`, `.map`)
- Build system files (`Makefile`, `lnkscript`, `make1.bat`)
- Documentation (`.docx` files)

### Assets
- `bitmaps/` - Original GBA graphics assets
- `TeamKNOx/` - GBA development library files

## Display Size

- **Advanced Version**: Now uses a large 800x600 window for modern screens. Board, menus, and fonts are all scaled up for better visibility.
- **Basic Version**: Uses a smaller window for simplicity.

## Running the Game

### Windows - Easy Launch (Recommended)
1. **Double-click** `play_reversi.bat` to run the advanced version directly
2. **Double-click** `run_reversi.bat` for a menu to choose between basic and advanced versions
3. **Right-click** `run_reversi.ps1` and select "Run with PowerShell" for the PowerShell version

### Command Line
```bash
# Basic Version
python reversi_pygame.py

# Advanced Version (Recommended)
python reversi_advanced.py
```

### PowerShell
```powershell
# Run advanced version
.\run_reversi.ps1

# Run basic version
.\run_reversi.ps1 -Version basic
```

## Game Controls

### Menu Navigation
- **Arrow Keys**: Navigate through menu options
- **Enter/Return**: Select option
- **Space**: Continue from opening screen
- **Left Arrow**: Go back in level selection

### Gameplay
- **Arrow Keys**: Move cursor on the board
- **Enter/Return**: Place stone (if valid move)
- **Close Window**: Quit game
- **Pass Turn**: If you have no valid moves, you will see "No valid moves! Press Enter to pass." Press Enter to pass your turn.

## Game Features

### Advanced Version Features
1. **Opening Screen**: Title screen with game name
2. **Color Selection**: Choose to play as Black or White
3. **Difficulty Selection**: Choose from Easy, Medium, or Hard
4. **Complete Game Logic**: Full Reversi rules implementation
5. **AI with Different Levels**:
   - **Easy**: Random valid moves
   - **Medium**: Basic minimax algorithm
   - **Hard**: Advanced minimax with corner evaluation
6. **Game Status Handling**: Pass moves, game end detection, and no more freezes
7. **Score Display**: Real-time score tracking
8. **Visual Feedback**: Different cursors for player vs AI turns
9. **Larger Display**: Modern, easy-to-read board and menus
10. **Improved Pass Logic**: If you have no valid moves, you must press Enter to pass, and the game will never freeze on AI thinking.

### Game Rules
- Players take turns placing stones on an 8x8 board
- Stones can only be placed where they can capture opponent stones
- Captured stones are flipped to the capturing player's color
- Game ends when no valid moves remain for both players
- Player with more stones wins

## Migration Details

The Pygame version maintains the same game logic and structure as the original GBA version. The original GBA source code and build artifacts are preserved in the `gba/` directory for reference.

### Preserved Elements
- **Constants**: All board dimensions, colors, and game states
- **Game Engine**: Complete Reversi logic including move validation and stone flipping
- **AI Algorithm**: Minimax implementation with corner evaluation
- **Game Flow**: Opening → Color Selection → Level Selection → Game
- **Visual Layout**: Similar board positioning and information display

### Adaptations for Pygame
- **Graphics**: Replaced GBA bitmap graphics with Pygame drawing functions
- **Input**: Converted GBA button input to keyboard controls
- **Display**: Adapted to standard desktop window instead of GBA screen
- **Timing**: Used Pygame's timing functions instead of GBA VBLANK

### Key Classes
- `ReversiEngine`: Core game logic and AI
- `ReversiGame`: Main game controller and UI
- `Evaluation`: Helper class for AI move evaluation

## Technical Notes

- The game uses the same 8x8 board size as the original
- AI difficulty levels correspond to search depth in the minimax algorithm
- Corner positions are weighted heavily in AI evaluation (25 points each)
- The game maintains the original GBA color scheme and layout proportions

## Bug Fixes & Improvements
- **No more freezes**: The game will always end if neither player can move, even in edge cases.
- **Explicit pass**: If you have no valid moves, you must press Enter to pass, and the game will show a clear message.
- **Larger display**: The advanced version is now much easier to play on modern screens.

## Future Enhancements

Potential improvements that could be added:
- Sound effects
- Save/load game states
- Network multiplayer
- Enhanced AI algorithms
- Custom board themes
- Replay functionality 