from pico2d import *
import gfw
import gobj

def collide(a,b):
	left_a,bottom_a,right_a,top_a = a.get_bb()
	left_b,bottom_b,right_b,top_b = b.get_bb()

	if left_a > right_b:return False
	if right_a < left_b:return False
	if top_a < bottom_b:return False
	if bottom_a > top_b:return False

	return True

def active_arrow(a,b):
	if b.name != 'arrow_block': return
	left_a,bottom_a,right_a,top_a = a.get_bb()
	left_b,bottom_b,right_b,top_b = b.get_active_bb()

	if left_a > right_b:return False
	if right_a < left_b:return False
	if top_a < bottom_b:return False
	if bottom_a > top_b:return False

	return True

def collide_check(player):
    collide_check_whip(player)
    collide_check_trap()
    collide_check_object(player)
    collide_check_monster(player)
    collide_check_score(player)

def collide_check_whip(player):
    # 채찍과 오브젝트 충돌체크
    for layer in range(gfw.layer.object, gfw.layer.score_object + 1):
        for obj in gfw.world.objects_at(layer):
            for i in gfw.world.objects_at(gfw.layer.whip):
                if obj.time < 1: continue
                crash = collide(obj,i)
                if crash == False: continue
                obj.collide_whip(player.pos)

    for obj in gfw.world.objects_at(gfw.layer.monster):
        for i in gfw.world.objects_at(gfw.layer.whip):
            crash = collide(obj,i)
            if crash == False: continue
            obj.dameged()

def collide_check_monster(player):
    # 플레이어와 몬스터 충돌체크 
    for M in gfw.world.objects_at(gfw.layer.monster):
        crash = collide(M,player)
        if crash == False: continue
        _,p_b,_,_ = player.get_bb()
        _, m_y = M.draw_pos
        if p_b > m_y:
            M.dameged()
            player.jump_speed = 1
        else:
            M.collide()
            player.dameged_just()

def collide_check_object(player):
    # 플레이어와 오브젝트 충돌체크 
    for obj in gfw.world.objects_at(gfw.layer.object):
        crash = collide(obj,player)
        if crash == False: continue
        dameged = obj.collide()
        if dameged == True:
            player.dameged_to_stun()

    # 몬스터와 오브젝트 충돌체크
    for obj in gfw.world.objects_at(gfw.layer.object):
        for m in gfw.world.objects_at(gfw.layer.monster):
            crash = collide(obj,m)
            if crash == False: continue
            m.dameged()

def collide_check_score(player):
    # 플레이어와 점수 충돌체크 
    for obj in gfw.world.objects_at(gfw.layer.score_object):
        crash = collide(obj,player)
        if crash == True:
            score = obj.collide()
            if obj.name == 'boom_pack':
                player.boom_count += score
            elif obj.name == 'rope_pack':
                player.rope_count += score
            else:
                player.increase_score(score)

def collide_check_trap():
    # 함정 발동 
    for layer in range(gfw.layer.object, gfw.layer.player + 1):
        for obj in gfw.world.objects_at(layer):
            for t in gfw.world.objects_at(gfw.layer.tile):
                crash = active_arrow(obj,t)
                if crash == True:
                    t.active()