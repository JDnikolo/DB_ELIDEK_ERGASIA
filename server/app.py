from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector


# configuration
DEBUG = True
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='test'
)
mycursor = mydb.cursor()

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def returnProjects():
    sql = 'select * from project '
    usewhere = False
    where = 'where '
    dur = request.args.get("duration")
    if dur != None and dur != '':
        op = '='
        if request.args.get("greater") == 'true':
            op = '>='
        if request.args.get("lesser") == 'true':
            op = '<='
        usewhere = True
        where = where + "timestampdiff(year, start_date, end_date) "+op+' '+dur
    fund_min = request.args.get('fund_min')
    if fund_min != '' and fund_min != None:
        if usewhere:
            where += ' and '
        else:
            usewhere = True
        where = where + " funds >= " + fund_min
    fund_max = request.args.get('fund_max')
    if fund_max != '' and fund_max != None:
        if usewhere:
            where += ' and '
        else:
            usewhere = True
        where = where + " funds < "+fund_max

    adminId = request.args.get("admin")
    if adminId != '' and adminId != None:
        if usewhere:
            where += ' and '
        else:
            usewhere = True
        where = where + 'admin_id = '+adminId

    active = request.args.get('active')
    inactive = request.args.get('inactive')
    if active != None and active == 'false':
        if usewhere:
            where += ' and '
        else:
            usewhere = True
        where = where + 'datediff(now() ,end_date)>0'
    if inactive != None and inactive == 'false':
        if usewhere:
            where += ' and '
        else:
            usewhere = True
        where = where + 'datediff(now() ,end_date)<=0'

    start = request.args.get('start')
    if start != '' and start != None:
        if usewhere:
            where += ' and '
        else:
            usewhere = True
        where = where + 'start_date >"{}-01-01"'.format(start)

    end = request.args.get('end')
    if end != '' and end != None:
        if usewhere:
            where += ' and '
        else:
            usewhere = True
        where = where + 'end_date <"{}-01-01"'.format(end)

    if usewhere:
        sql = sql+where
    print(sql)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return jsonify(myresult)


@app.route('/admins', methods=['GET'])
def returnAdmins():
    # only returns admins that are on projects
    sql = 'select  p.admin_id ,ea.name,ea.surname from project p inner join elidek_admin ea where p.admin_id = ea.admin_id group by name'
    print(sql)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return jsonify(myresult)


@app.route('/staff', methods=['GET'])
def returnStaff():
    projectId = request.args.get('project')
    directorID = request.args.get('director')
    sql = 'select name,surname from researcher r where r_id = {}'.format(
        directorID)
    print(sql)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    sql = 'select name,surname from works_in wi join researcher r  where e_id={} and wi.r_id =r.r_id'.format(
        projectId)
    print(sql)
    mycursor.execute(sql)
    myresult.append(mycursor.fetchall())
    return jsonify(myresult)


@app.route('/fields', methods=['GET'])
def returnFields():
    mycursor.execute('select * from research_field rf')
    results = mycursor.fetchall()
    result = []
    for a in results:
        result.append(a[0])
    print('select * from research_field rf')
    return jsonify(result)


@app.route('/byField', methods=['GET'])
def returnByField():
    sql = 'select * from project p'
    join = ''
    where = ''
    mode = request.args.get('mode')
    name = request.args.get('name')
    since = request.args.get('since')
    if mode == 'project':
        join = ' join part_of po on p.e_id =po.e_id '
        where = ' where po.Name ="{}"'.format(name)
        if since != None and since != '':
            where += ' and p.start_date<"{}-1-1" and p.end_date>"{}-1-1"'.format(
                since, since)

    if mode == 'researcher':
        p1 = ''
        p2 = ''
        if since != None and since != '':
            p1 = 'and p.start_date<"{}-1-1" and p.end_date>"{}-1-1"'.format(
                since, since)
            p2 = ' and date_since <"{}-1-1"'.format(since)
        sql = '''select * from researcher r where r.r_id in 
(select wi.r_id from works_in wi join project p on p.e_id=wi.e_id 
where p.e_id in (select e_id from part_of po where po.Name='{}'){}){}'''.format(name, p1, p2)
    sql = sql+join+where
    print(sql)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return jsonify(myresult)


@app.route('/byProjCount', methods=['GET'])
def returnOrgsByProjectCount():
    result = []
    having = ''
    connect = ''
    select = 'count(*) as proj1, '
    having = 'having '

    year = request.args.get('year')
    if year != None and year != '':
        select = 'COUNT(IF(year(p.start_date)={}, 1, NULL)) as proj1, '.format(
            year)
        if request.args.get('consecutive') == 'true':
            select += 'COUNT(IF(year(p.start_date)={}, 1, NULL)) as proj2, '.format(int(year)+1)
            if request.args.get('equal') == 'true':
                having += 'proj1=proj2'
                connect = ' and '

    if request.args.get('num') != None:
        having += ' {} proj1'.format(connect)
        comp = ''
        if request.args.get('more') == 'true':
            comp += '>'
        if request.args.get('less') == 'true':
            comp += '<'
        having += '{}={}'.format(comp, request.args.get('num'))
        connect = ' and '
        if request.args.get('consecutive') == 'true':
            having += '{} proj2{}={}'.format(connect,
                                             comp, request.args.get('num'))
    if having == 'having ':
        having = 'having proj1>0 '
    sql = '''select {} o.* from organization o 
join project p on p.abrv = o.abrv 
group by o.abrv {} order by proj1 desc '''.format(select, having)
    print(sql)
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return jsonify(result)


@app.route('/fieldPairs', methods=['GET'])
def returnFieldPairs():
    where = 'where p.e_id=po.e_id and '
    usewhere = False
    active = request.args.get('active')
    inactive = request.args.get('inactive')
    if active != None and active == 'false':
        usewhere = True
        where = where + \
            'datediff(now() ,end_date)>0 '
    if inactive != None and inactive == 'false':
        if usewhere:
            where += ' and '
        else:
            usewhere = True
        where = where + \
            'datediff(now() ,end_date)<=0 and datediff(now() ,start_date)>0 '
    if usewhere:
        subquery = 'where exists (select * from project p {}) '.format(where)
    else:
        subquery = ''
    sql = '''SELECT count(*)as num,
   CASE WHEN po.Name >po2.Name  THEN po2.Name  ELSE po.Name  END as name1,
   CASE WHEN po.Name < po2.Name THEN po2.Name ELSE po.Name END as name2
FROM part_of po join part_of po2
on po.Name !=po2.Name  and po.e_id =po2.e_id 
{}
group by name1 order by num desc'''.format(subquery)
    print(sql)
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return jsonify(result)


@app.route('/researchers', methods=['GET'])
def returnResearchers():
    sql = 'select r_id,name,surname from researcher r '
    where = ''
    usewhere = False
    age = request.args.get('age')
    if age != None:
        where = ' where '
        usewhere = True
        op = ''
        if request.args.get('more') == 'true':
            op += '>'
        if request.args.get('less') == 'true':
            op += '<'
        op += '='
        where += 'timestampdiff(year,r.date_of_birth,now()){}{} '.format(op, age)
    proj = request.args.get('byProj')
    active = request.args.get('byActive')
    exclude = request.args.get("exclude")
    extrajoin = ''
    if active == 'true':
        proj = 'true'
        extrajoin = 'join project p ON wi.e_id =p.e_id'
        if usewhere:
            where += ' and p.start_date <now() and p.end_date >now()'
        else:
            usewhere = True
            where += ' where p.start_date <now() and p.end_date >now()'
    age = request.args.get('byAge')
    extraorder = ''
    if age == 'true':
        extraorder = 'age,'
    if proj == 'true':
        if exclude == 'true':
            if usewhere:
                where += '''and wi.e_id in(
select p.e_id  from project p 
where p.e_id not in (select e_id from deliverable d)) '''
            else:
                usewhere = True
                where = '''where wi.e_id in(
select p.e_id  from project p 
where p.e_id not in (select e_id from deliverable d)) '''
        sql = '''select count(*) as projs,r.name ,r.surname, timestampdiff(year,r.date_of_birth,now()) as age  from researcher r
join works_in wi
on wi.r_id =r.r_id 
{}
{}
group by r.surname,r.name
order by {}projs desc'''.format(extrajoin, where, extraorder)
    else:
        sql = 'select r_id,name,surname,timestampdiff(year,r.date_of_birth,now()) as age from researcher r {} order by {}r_id '.format(
            where, extraorder)
    print(sql)
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return jsonify(result)


@app.route('/adminsByFunds', methods=['GET'])
def returnAdminsByFunds():
    where = ''
    org = request.args.get("org")
    if org != None and org != '':
        where += ' where o.abrv="{}"'.format(org)
    sql = '''select ea.name,ea.surname,p.abrv,o.full_name,SUM(p.funds) as total from project p 
join elidek_admin ea 
on p.admin_id =ea.admin_id 
join organization o 
on p.abrv =o.abrv 
{}
group by name,surname,abrv 
order by total desc'''.format(where)
    print(sql)
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return jsonify(result)


@app.route('/orgs', methods=['GET'])
def returnOrganisations():
    # returns all organizations
    sql = 'select abrv,full_name from organization o'
    print(sql)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return jsonify(myresult)


@app.route('/programs', methods=['GET'])
def returnPrograms():
    # returns ELIDEK programs
    sql = 'select * from elidek_program ep'
    print(sql)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return jsonify(myresult)


@app.route('/projectOfProgram', methods=['GET'])
def returnProjectsOfProgram():
    # all projects that are part of an ELIDEK program.
    p_id = request.args.get('p_id')
    sql = 'select * from project p where p.p_id = {}'.format(p_id)
    print(sql)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return jsonify(myresult)


@app.route('/projectPerResearcher', methods=['GET'])
def returnProjectsPerResearcher():
    order = ''
    where = ''
    proj = request.args.get('byProj')
    if proj == 'true':
        order = 'order by title'
    name = request.args.get('byName')
    if name == 'true':
        if order != '':
            order += ',surname,name'
        else:
            order = 'order by surname,name'
    active = request.args.get('active')
    inactive = request.args.get('inactive')
    if active == 'false':
        where = 'where datediff(now() ,end_date)>0'
    if inactive == 'false':
        if where != '':
            where += ' and datediff(now() ,end_date)<=0 and datediff(now() ,start_date)>=0 '
        else:
            where = 'where datediff(now() ,end_date)<=0 and datediff(now() ,start_date)>=0'
    sql = 'select * from projects_per_researcher ppr {} {}'.format(
        where, order)
    print(sql)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return jsonify(myresult)


@app.route('/projectGradeEvaluators', methods=['GET'])
def projectGradeEvaluators():
    where = ''
    order = ''
    byGrade = request.args.get('byGrade')
    byName = request.args.get('byName')
    if byGrade == 'true':
        order = 'order by grade'
    proj = request.args.get('byProj')
    if proj == 'true':
        if order != '':
            order += ',title'
        else:
            order = 'order by title'
    if byName == 'true':
        if order != '':
            order += ',surname,name'
        else:
            order = 'order by surname,name'

    name = request.args.get('name')
    if name != '' and name != None:
        where = 'where LOCATE("{}",title)>0 '.format(name)

    sql = 'select * from project_evaluators pe {} {}'.format(where, order)
    print(sql)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return jsonify(myresult)


if __name__ == '__main__':
    app.run()
