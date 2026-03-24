def format_instruction(freq, dose, drug_name, period_type="Günde"):
    """
    Takes raw frequency and dose from Medula and formats them into a clean string
    e.g. freq="2", dose="1.0", drug="YASMIN 21 FILM TABLET" -> "Sabah 1 tablet, Akşam 1 tablet"
    """
    
    # Normalizing drug name
    name_upper = str(drug_name).upper()
    
    # Determine Unit type and context based on drug keywords
    unit = "doz"
    if any(kw in name_upper for kw in ["ŞURUP", "SÜSPANSİYON", "SÜSP", "ŞAŞE"]):
        unit = "ölçek"
    elif any(kw in name_upper for kw in ["DAMLA", "GTT"]):
        unit = "damla"
    elif any(kw in name_upper for kw in ["SPREY", "İNHALER", "PUF", "AEROSOL"]):
        unit = "puf"
    elif any(kw in name_upper for kw in ["KREM", "JEL", "MERHEM", "POMAD", "LOSYON"]):
        unit = "kez sürülür"
    elif any(kw in name_upper for kw in ["KAPSÜL", "TABLET", "DRAJE", "FİLM"]):
        unit = "tablet"
        
    # Formatting the dose
    d_str = str(dose).replace(',', '.')
    try:
        d = float(d_str)
        if d.is_integer():
            d_str = str(int(d))
    except ValueError:
        pass # Not a straightforward float, leave it as is
        
    f_str = str(freq).strip()
    
    # Some generic forms
    if period_type.strip().lower() != "günde":
        return f"{period_type} {f_str} kere {d_str} {unit}"
        
    # Standard daily forms
    if f_str == "1":
        if "sürülür" in unit:
            return f"Günde 1 {unit}"
        return f"Sabah {d_str} {unit}"
    elif f_str == "2":
        if "sürülür" in unit:
            return f"Sabah {d_str}, Akşam {d_str} {unit}"
        return f"Sabah {d_str} {unit}, Akşam {d_str} {unit}"
    elif f_str == "3":
        if "sürülür" in unit:
            return f"Sabah {d_str}, Öğle {d_str}, Akşam {d_str} {unit}"
        return f"Sabah {d_str} {unit}, Öğle {d_str} {unit}, Akşam {d_str} {unit}"
    elif f_str == "4":
        if "sürülür" in unit:
            return f"Sabah {d_str}, Öğle {d_str}, Akşam {d_str}, Gece {d_str} {unit}"
        return f"Sabah {d_str} {unit}, Öğle {d_str} {unit}, Akşam {d_str} {unit}, Gece {d_str} {unit}"
    
    # Fallback if frequency is weird (like 5 or 0)
    return f"Günde {f_str} defa {d_str} {unit}"
