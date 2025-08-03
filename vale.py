from math import sin, cos, radians
def predict(enlem, boylam, irtifa, dikilme, yonelme, yatis, hiz, zaman=0.5):
  vx = zaman*hiz*cos(radians(dikilme))
  vy = zaman*hiz*sin(radians(dikilme))*sin(radians(yatis))
  vz = zaman*hiz*sin(radians(dikilme))*cos(radians(yatis))

  
    
  delta_boylam_metre = vx*cos(radians(yonelme)) - vy*sin(radians(yonelme))
  delta_enlem_metre = vx*sin(radians(yonelme)) - vy*cos(radians(yonelme))
  delta_irtifa = vz

  boylam_destek = 111320 * cos(radians(enlem))
  delta_boylam = delta_boylam_metre / boylam_destek
  delta_enlem = delta_enlem_metre / 111132

  yeni_enlem = enlem+delta_enlem
  yeni_boylam = boylam+delta_boylam
  yeni_irtifa = irtifa+delta_irtifa

  #print("Enlem:",yeni_enlem,"Boylam:",yeni_boylam,"irtifa:",yeni_irtifa)
  return yeni_enlem, yeni_boylam, yeni_irtifa
