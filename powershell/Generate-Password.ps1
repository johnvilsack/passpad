# Password Generator - PowerShell Implementation
# Based on EFF Short Wordlist

# Load wordlist from local file
$DicewareList = @{}
try {
    $wordlistPath = Join-Path $PSScriptRoot "../eff_short_wordlist_1.txt"
    if (-not (Test-Path $wordlistPath)) {
        throw "wordlist.txt not found"
    }
    
    Get-Content $wordlistPath | ForEach-Object {
        $line = $_.Trim()
        if ($line -and $line.Contains("`t")) {
            $parts = $line -split "`t"
            if ($parts.Length -eq 2) {
                $DicewareList[$parts[0]] = $parts[1]
            }
        }
    }
    
    if ($DicewareList.Count -eq 0) {
        throw "No valid entries found in file"
    }
} catch {
    Write-Error "Failed to load wordlist: $_"
    exit 1
}

function Get-DicewareWord {
    for ($i = 0; $i -lt 20; $i++) {
        $roll = -join (1..4 | ForEach-Object { Get-Random -Minimum 1 -Maximum 7 })
        if ($DicewareList.ContainsKey($roll)) {
            return $DicewareList[$roll]
        }
    }
    return "word"
}

function New-Password {
    # Generate 4 diceware words
    $words = @()
    for ($i = 0; $i -lt 4; $i++) {
        $words += Get-DicewareWord
    }
    
    # Capitalize first word
    $words[0] = $words[0].Substring(0,1).ToUpper() + $words[0].Substring(1)
    
    # Generate random number (10-99)
    $number = Get-Random -Minimum 10 -Maximum 100
    
    # Generate random special character
    $specials = "!@#$%^&*?".ToCharArray()
    $special = $specials | Get-Random
    
    # Combine all parts
    return "$($words -join '-')-$number$special"
}

# Generate and return password
New-Password